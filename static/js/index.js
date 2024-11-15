let firstQuestionBool = true;
let currentQuestion = "";

function answerQuestion()
{
    const question = document.getElementById('question_box').value;
    fetch('/askChatGPT', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question })
    })
    .then(response => response.json())
    .then(data => {
        const answer = data.response;
        document.getElementById('answer_box').value = answer;
        addHistory(question, answer);
    })
    .catch(error => console.error("ERROR - ", error));   
}

function addHistory(question, answer)
{
    if(!firstQuestionBool)
    {
        const historyBoxContents = document.getElementById('history_box').value;
        const history = historyBoxContents == "" ? currentQuestion : historyBoxContents + currentQuestion;
        document.getElementById('history_box').value = "";
        document.getElementById('history_box').value = history;
    }

    currentQuestion = "Question : " + question + '\n\n' + "Answer : " + answer + '\n\n' + "=".repeat(40) + '\n\n';
    firstQuestionBool = false;
}

function clearBox(box) {
    box.value = "";
}

function changeLanguage(language)
{
    switch(language)
    {
        case "en":
            document.getElementById("title").innerHTML = "Business Negotiation Chatbot";
            document.getElementById("input_title").innerHTML = "Question Input";
            document.getElementById("question_btn").innerHTML = "Generate Answer";
            document.getElementById("output_title").innerHTML = "Answer Output";
            document.getElementById("history_title").innerHTML = "Chat History";
            break;

        case "jp":
            document.getElementById("title").innerHTML = "ビジネス交渉　チャットボット";
            document.getElementById("input_title").innerHTML = "質問入力";
            document.getElementById("question_btn").innerHTML = "質問を聞く";
            document.getElementById("output_title").innerHTML = "答え出力";
            document.getElementById("history_title").innerHTML = "チャット歴史";
            break;

        case "zh":
            document.getElementById("title").innerHTML = "商務談判網路聊天系統";
            document.getElementById("input_title").innerHTML = "問題輸入";
            document.getElementById("question_btn").innerHTML = "生成答案";
            document.getElementById("output_title").innerHTML = "答案輸出";
            document.getElementById("history_title").innerHTML = "聊天記錄";
            break;
    }
}