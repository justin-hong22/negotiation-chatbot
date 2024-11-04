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
        document.getElementById('answer_box').value = data.response;

        const answer = document.getElementById('answer_box').value;
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

    currentQuestion = "Question : " + question + '\n\n' + "Answer : " + answer + '\n\n' + "=".repeat(150) + '\n\n';
    firstQuestionBool = false;
}
