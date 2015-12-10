@echo off
cd "C:\Users\Av\Documents\GitHub\tutoring_reports"
git pull
runipy "C:\Users\Av\Documents\GitHub\tutoring_reports\report.ipynb" "C:\Users\Av\Documents\GitHub\tutoring_reports\report.ipynb"
git add .
git commit -am "new report"
git push
pause
