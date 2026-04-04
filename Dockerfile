#設計目的:
#把這個 image 做成「可直接執行的 CLI 工具」


FROM python:3.11-slim 
#建立一個以 Python 3.11 為基底的 Docker 環境

WORKDIR /app
#把接下來工作的目錄設定成 /app。

COPY src/ /app/src/
#只把專案裡的 src/ 資料夾，複製到容器內的 /app/src/。

WORKDIR /app/src
#把目前工作目錄再切到 /app/src。

ENTRYPOINT ["python", "-m", "elysia_core.cli"]
#容器啟動時，主要執行的程式就是 python -m elysia_core.cli

CMD [""]
#提供一個預設參數給 ENTRYPOINT，有參數則覆蓋，無參數則帶入""