# PDFs-AI-rename

A quick and creative way to rename messy PDF files. Saving your precious time.

Here's how it works:

1. **Read PDFs**: The script scans a specified folder on your computer, looking for PDF files. It then reads the text from each PDF, Extracting the information on the first page of your PDFs that will inspire the new file names.

2. **Generate Names**: With the content of your PDFs in hand, the script sends a message to a smart AI service. This AI takes the content, thinks about it, and comes up with a short, catchy name for each file – no more than 5 keywords, contacted by `_`, such as `A_numpy_cheatsheet`.

3. **Rename Files**: Once the AI has suggested new names, the script goes back to your folder and renames each PDF accordingly. Now, instead of generic names like "document1.pdf" or "report.pdf," you have meaningful, concise titles that reflect the content of each file.


## Install
- 💻 Install `PyPDFs` and `groq` use command line  

```
pip install PyPDF2 groq
```

- 🔑 Get your Groq AI KEY [here](https://console.groq.com/keys)  

- 📝 open `.zshrc` file.
For Mac user, it's a hidden path under your username, like `/Users/jerlin/.zshrc`, check it by keyboard shortcut `Shift + CMD + .`
  
Fill the code and save:  
```
GROQ_API_KEY="REPLACE YOUR KEY"
```

## Todo
- [ ] Clean up unanticipated characters such as `\`.
- [ ] Pretty rename, no more cutting of keyword.
- [ ] Rename by LMM such as LlaVa or Gemini Pro Vision.(Also FREE). 
- [ ] Say googbye to command line: release a Mac Automatic Flow,  which use the `RIGHT CLICK` instead, as the example shown below.

## Example  
https://github.com/jerlinn/PDFs-AI-rename/assets/91647085/bf49fdae-0709-4bea-8106-ec98167affb6

**Have fun with AI Copilots**
- 微信视频号 @oasisAI
- 微信号 oasisFM
