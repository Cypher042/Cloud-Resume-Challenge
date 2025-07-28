

window.addEventListener('DOMContentLoaded', (event) => {
    // Initialize the visit count when the DOM is fully loaded
    getVisitCount();
});



const functionApiURL = window.env.FUNCTION_API_URL;

const getVisitCount = () => {
    let count = 30;
    fetch(functionApiURL).then(response => {
        return response.json();
    }).then(response => {

        console.log("function callewd: " + response);
        count = response.count;
        document.getElementById("counter").innerText = count;
    }).catch(error => {
        console.error("Error fetching visit count:", error);
    });

    return count;
 
}