from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass
class StoneInput:
    report_number: str
    shape: str
    crown_angle: float
    pavilion_angle: float
    table_percent: float
    depth_percent: float
    crown_percent: float
    pavilion_percent: float
    girdle_percent: float

    @classmethod
    def from_row(cls, row):
        return cls(
            report_number=str(row.get("Report #", "")),
            shape=str(row.get("Shape", "ROUND")).upper(),
            crown_angle=float(row["CrownAngle"]),
            pavilion_angle=float(row["PavilionAngle"]),
            table_percent=float(row["TablePercent"]),
            depth_percent=float(row["DepthPercent"]),
            crown_percent=float(row["CrownPercent"]),
            pavilion_percent=float(row["PavilionPercent"]),
            girdle_percent=float(row["GirdlePercent"]),
        )

    def to_engine_kwargs(self) -> Dict[str, float]:
        return {
            "crown_a": self.crown_angle,
            "pav_a": self.pavilion_angle,
            "table": self.table_percent,
            "depth": self.depth_percent,
            "crown_p": self.crown_percent,
            "pav_p": self.pavilion_percent,
            "girdle_p": self.girdle_percent,
        }

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
