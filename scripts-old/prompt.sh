pip install -U pip

if [ -n "$EXPERIMENTAL" ]; then
    pip install -U transformers~=4.36.2 tiktoken~=0.5.2 torch~=2.1.2 accelerate~=0.26.1
else
    pip install -U g4f~=0.2.0.3
fi

mkdir -p ./tmp
if [ -n "$EXPERIMENTAL" ]; then
    if [ -n "$PROMPT" ]; then
        python experimental-prompt.py $CONFIGPATH "$PROMPT"
    else 
        python experimental-prompt.py $CONFIGPATH 
    fi
else
    if [ -n "$PROMPT" ]; then
        python prompt.py $CONFIGPATH "$PROMPT"
    else 
        python prompt.py $CONFIGPATH
    fi
fi