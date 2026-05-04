@echo off
chcp 65001 >nul
echo ============================================
echo  Сброс активного контекста quest workflow
echo ============================================
echo.

set "CONTEXT_FILE=workspace\active_context.json"

if exist %CONTEXT_FILE% (
    del %CONTEXT_FILE%
    echo [OK] Файл %CONTEXT_FILE% удалён.
) else (
    echo [INFO] Файл %CONTEXT_FILE% уже отсутствует.
)

echo.
echo Контекст сброшен. Можно начинать новую campaign.
echo.
pause
