from pathlib import Path

pdf_path = Path("data/거래명세서_정하람_과장_물류팀.pdf")

with open(pdf_path, "rb") as f:
    file_bytes = f.read()

document_dummy_data = [
    {
        "제목": "ERP 거래명세서",
        "파일명": "ERP_거래명세서_정하람_과장_물류팀.pdf",
        "업로더": "정하람 (과장 / 물류팀)",
        "등록일": "2025-06-17",
        "파일데이터": file_bytes,
        "요약": "금강소재와의 거래로, 알루미늄/철판/동판 납품 내역이 포함된 거래명세서입니다.",
        "임베딩": [],
        "본문": "문서번호: TX-2025-0122-005\n거래일자: 2025-01-22\n품목: 알루미늄 0.8T 외 2건\n총 거래액: 약 98만원"
    }
]
