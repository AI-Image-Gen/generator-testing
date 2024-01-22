# 🍹 Table of usage
## 🛸 Custom settings.json file

🚀 **Look at [`config/settings.json`](https://github.com/AI-Image-Gen/generator/blob/main/config/settings.json) as template**

<details style="border: 1px solid #006400; border-radius: 10px; padding: 7px; margin-bottom: 10px">
<summary> 📖 Variables</summary>

## 📔 Types of data
| 🔢 Input      | 🛸 Type | 🔥 Inputs              |
|:-------------:|:-------:|:----------------------:|
|`bool`         | boolean | `true` or `false`      | 
|`int`          | integer | any `number`           | 
|`str`          | string  | any `characters`       | 
|`arr`          | array   | array of some `input`s | 

## 💬 Input strings
🌐 *Example use:*
```json\n"input": "{REPO}"\n```

| 🔢 Input {}   | 🛸 Meaning              | 🔥 Side notes   |
|:-------------:|:-----------------------:|:---------------:|
|`REPO`         | `str` repository path   |<details><summary>Example</summary> `"repo/path"`</details>|

<details style="border: 1px solid #8B8000; border-radius: 10px; padding: 7px; margin-bottom: 10px">
<summary>

```json\n"input": "{config.Input}"\n```
</summary>

| 🔢 Input | 🛸 Meaning           |🔥 Side notes         |
|:------------------:|:--------------------:|:--------------------:|
|`mix0`              | Outputs amount `arr` | <details><summary>Example</summary>`[0, 1]` for <br>`out_amount: 2`</details>|
|`mix1`              | mix0 + previous ai amount `arr`     | 
|`mix2`              | mix1 + previous ai amount `arr`     | 

<details style="border: 1px solid #00008B; border-radius: 10px; padding: 7px">
<summary>

```json\n"input": "{config.models.Input}"\n```
</summary>

🚀 *Will be generated from config/models.json*

| 🔢 Input | 🛸 Meaning           |🔥 Side notes         |
|:------------------:|:--------------------:|:--------------------:|
|`txt2img`              | txt2img supported AI models `arr` | <details><summary>Example</summary>`["sd-v1.5"]`</details>|
|`img2img`              | img2img supported AI models `arr`     | 
|`img_upscale`              | img_upscale supported AI models `arr` | 
|`img2vid`              | img2vid supported AI models `arr`     | 

</details>
</details>

<details style="border: 1px solid #8B8000; border-radius: 10px; padding: 7px">
<summary>

```json\n"input": "{txt2txt.Input}"\n```
</summary>

🚀 *Will be generated from config/models.json*

| 🔢 Input | 🛸 Meaning           |🔥 Side notes         |
|:------------------:|:--------------------:|:--------------------:|
|`prompt`              | AI optimized prompt `str` | <details><summary>Example</summary>`"Generate something"`</details>|


</details>



</details>  


🚨 *Default values are used in **previews***  

```json\n{"global": {},\n"txt2txt": {},\n"txt2img": {},\n"img2img": {},\,"img_upscale": {},\n"img2vid": {}\n}\n```

<details style="border: 1px solid #8B8000; border-radius: 10px; padding: 7px">
<summary>

```json\n"global": {\n"clean_artifacts": true,\n"out_amount": 1,\n"push": {}\n}\n```
</summary>

| ⚡ Setting      | 🔢 Input          | 🔥 Description  |
|:----------------:|:------------------:|:--------------:|
|`clean_artifacts`| `bool`             | Delete temporary artifacts?| 
|`out_amount`| `int`<br>in **1**-**10** range    | How many prompts should be called?<details style="border: 1px solid; border-radius: 10px; padding: 2px"><summary>*Limitations* 🚧</summary>Edit available only with<br>**txt2txt** `active: true`</details> | 

<details style="border: 1px solid #006400; border-radius: 10px; padding: 7px">
<summary>

```json\n"push": {\n"active": true,\n"imgs_dir": "{REPO}/content/img",\n"vids_dir": "{REPO}/content/vid",\n"prompt_dir": "{REPO}/content/prompts",\n}\n```

</summary>

| ⚡ Setting      | 🔢 Input          | 🔥 Description |
|:---------------:|:------------------:|:---------------|
|`active`| `bool` | Push to repository? |
|`imgs_dir`| `str` | Images push path  |
|`vids_dir`| `str` | Videos push path  |
|`prompt_dir`| `str` | Prompts push path  |

</details>

</details>