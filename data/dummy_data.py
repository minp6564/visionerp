
import pandas as pd
from datetime import datetime, timedelta

base_time = datetime.now()

inventory_logs = pd.DataFrame([
    {
        "날짜": (base_time - timedelta(days=2)).strftime("%Y-%m-%d %H:%M"),
        "품목명": "철판 1.2T",
        "구분": "입고",
        "수량": 100,
        "입고단가": 1200,
        "출고단가": 0,
        "마진율": "",
        "납품업체명": "ABC상사",
        "담당자명": "홍길동",
        "비고": "초기 입고"
    },
    {
        "날짜": (base_time - timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
        "품목명": "철판 1.2T",
        "구분": "출고",
        "수량": 20,
        "입고단가": 1200,
        "출고단가": 1800,
        "마진율": 50.0,
        "납품업체명": "ABC상사",
        "담당자명": "이철수",
        "비고": "초도 납품"
    }
])
