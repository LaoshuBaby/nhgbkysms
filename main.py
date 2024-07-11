from fastapi import FastAPI
import random

app = FastAPI()


@app.get("/random-number")
def read_random_number():
    random_number = random.randint(1, 30)
    return {
        "random_number": random_number,
        "note": """```Q
假如"日本語"可以缩写为nhg，因为nihongo

那么"日本語を勉強します"可以怎么缩写
```

```A
如果按照你给出的逻辑，将“日本語”缩写为“nhg”，我们可以尝试用同样的方法缩写“日本語を勉強します”。在这里，“を”是助词，可以 省略；“勉強します”是动词“勉強する”的敬体形式。

“勉強します”可以分解为“勉強（benkyou）”和“します（shimasu）”，所以我们可以提取每个单词的首字母来缩写：

- 日本語（にほんご）→ nhg
- 勉強（べんきょう）→ bky
- します（します）→ sms

因此，“日本語を勉強します”可以缩写为：

**nhg bky sms**
```""",
    }
