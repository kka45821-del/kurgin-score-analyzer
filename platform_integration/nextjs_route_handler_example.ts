// Example Next.js route handler for KURGIN Platform.
// Place in: app/api/tools/kurgin-score/analyze/route.ts

import { NextRequest, NextResponse } from "next/server";
import { KurginFormulaApiClient } from "@/lib/kurgin/formula_api_client";

export async function POST(request: NextRequest) {
  const body = await request.json();

  const client = new KurginFormulaApiClient({
    baseUrl: process.env.KURGIN_FORMULA_API_URL!,
    apiKey: process.env.KURGIN_FORMULA_API_KEY!,
  });

  try {
    const result = await client.analyzeStone(body.stone, body.language ?? "RU");
    return NextResponse.json(result);
  } catch (error) {
    return NextResponse.json(
      { status: "ERROR", error: "Formula API request failed" },
      { status: 500 },
    );
  }
}
