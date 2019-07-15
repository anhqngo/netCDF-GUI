# I have to write this command manually because vscode for some reason does
# not recognize autopep8 tool
autopep8 --in-place --aggressive --aggressive src/main/python/main.py

for file in $(find src/main/python/utils -name '*.py'); 
do 
autopep8 --in-place --aggressive --aggressive $file 
done