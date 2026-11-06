# Web app C# (.NET 10) — build từ gốc repo để dùng chung templates/ và content/
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src
COPY webapp/VietCv.Web.csproj webapp/
RUN dotnet restore webapp/VietCv.Web.csproj
COPY webapp/ webapp/
COPY templates/ templates/
COPY content/ content/
RUN dotnet publish webapp/VietCv.Web.csproj -c Release -o /app/publish /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/aspnet:10.0

# Chromium: bản Ubuntu chỉ có snap -> dùng chrome-headless-shell chính thức của Chrome for Testing
# (cùng engine in PDF, không kéo GTK/X11/DRM của Chrome đầy đủ). Cài + dọn trong 1 layer để không phình image.
# fonts-liberation đủ dấu tiếng Việt; fonts-crosextra-carlito để hệ thống khớp font 'Calibri' như máy dev;
# poppler-utils để đọc PDF tải lên; gosu để hạ quyền sau khi chown /data.
RUN apt-get update && apt-get install -y --no-install-recommends \
      wget unzip ca-certificates \
      libnss3 libnspr4 libasound2t64 libatk1.0-0t64 libatk-bridge2.0-0t64 \
      libatspi2.0-0t64 libcups2t64 libdrm2 libgbm1 libxkbcommon0 libxcomposite1 \
      libxdamage1 libxfixes3 libxrandr2 libx11-6 libxcb1 libxext6 libxi6 libxrender1 \
      libdbus-1-3 libexpat1 libsystemd0 libglib2.0-0 \
      fonts-liberation fonts-crosextra-carlito poppler-utils gosu \
    && mkdir -p /opt/chrome \
    && wget -qO /tmp/chs.zip "https://storage.googleapis.com/chrome-for-testing-public/157.0.8103.38/linux64/chrome-headless-shell-linux64.zip" \
    && unzip -q /tmp/chs.zip -d /tmp/chs \
    && cp -a /tmp/chs/chrome-headless-shell-linux64/. /opt/chrome/ \
    && rm -rf /tmp/chs /tmp/chs.zip /opt/chrome/locales/* \
    && apt-get purge -y --auto-remove wget unzip \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/* /usr/share/doc/* /usr/share/man/*

ENV CHROME=/opt/chrome/chrome-headless-shell \
    DATA_DIR=/data \
    ASPNETCORE_URLS=http://0.0.0.0:8080 \
    DOTNET_RUNNING_IN_CONTAINER=true

WORKDIR /app
COPY --from=build /app/publish .
COPY webapp/docker-entrypoint.sh /app/docker-entrypoint.sh
RUN mkdir -p /data && chmod +x /app/docker-entrypoint.sh
VOLUME ["/data"]
EXPOSE 8080
# root -> chown /data theo PUID/PGID -> hạ xuống user app (xem docker-entrypoint.sh)
ENTRYPOINT ["/app/docker-entrypoint.sh", "dotnet", "VietCv.Web.dll"]
