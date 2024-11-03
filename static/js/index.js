function answerQuestion()
{
    const question = document.getElementById('question_box').value;
    fetch('/askChatGPT', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question })
    })
    .then(response => response.json())
    .then(data => {document.getElementById('answer_box').value = data.response; })
    .catch(error => console.error("ERROR - ", error));
}