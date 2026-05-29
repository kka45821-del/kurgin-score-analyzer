// TypeScript client for KURGIN Formula API.
// Intended for KURGIN Platform backend/server route usage, not direct browser calls.

export type KurginStoneInput = Record<string, unknown>;

export interface KurginFormulaClientOptions {
  baseUrl: string;
  apiKey?: string;
}

export class KurginFormulaApiClient {
  private baseUrl: string;
  private apiKey?: string;

  constructor(options: KurginFormulaClientOptions) {
    this.baseUrl = options.baseUrl.replace(/\/$/, "");
    this.apiKey = options.apiKey;
  }

  private headers(): HeadersInit {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };
    if (this.apiKey) headers["X-KURGIN-API-Key"] = this.apiKey;
    return headers;
  }

  async health() {
    const res = await fetch(`${this.baseUrl}/v1/health`, { cache: "no-store" });
    if (!res.ok) throw new Error(`KURGIN health failed: ${res.status}`);
    return res.json();
  }

  async analyzeStone(stone: KurginStoneInput, language = "RU") {
    const res = await fetch(`${this.baseUrl}/v1/analyze/stone`, {
      method: "POST",
      headers: this.headers(),
      body: JSON.stringify({ language, stone }),
      cache: "no-store",
    });
    if (!res.ok) throw new Error(`KURGIN analyze failed: ${res.status} ${await res.text()}`);
    return res.json();
  }
}
