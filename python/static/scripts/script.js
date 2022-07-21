// ============= DEFINING CONSTANTS =============
const predictionApiUrl = "http://localhost:5000/api/v1/get_prediction";

$(document).ready(function () {
    // Predict button onclick
    $("#predict-button").click(function () {
        checkInputParameters();
    });
});

function checkInputParameters() {
    let postData = {
        ticketClass: parseInt(
            $("#ticket-class-select").find(":selected").val()
        ),
        age: parseInt($("#age-input").val()),
        sex: $("#sex-select").find(":selected").val(),
        sibsp: parseInt($("#sibsp-input").val()),
        parch: parseInt($("#parch-input").val()),
        fare: parseFloat($("#fare-input").val()),
        embarked: $("#embarked-select").find(":selected").val(),
    };

    let allInputsAreFilled = true;
    for (const [key, val] of Object.entries(postData)) {
        if (val === "") {
            alert("One or more inputs are empty. Please fill in all inputs.");
            allInputsAreFilled = false;
            break;
        }
    }

    if (allInputsAreFilled) {
        // POST request
        $("#prediction").addClass("hide");
        $("#prediction").text("");
        fetch(predictionApiUrl, {
            method: "POST",
            headers: {
                Accept: "*/*",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(postData),
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                if (!data.isError) {
                    if (data.prediction === 1) {
                        $("#prediction").text("SURVIVED");
                    } else {
                        $("#prediction").text("DID NOT SURVIVE");
                    }
                    $("#prediction").removeClass("hide");
                } else {
                    alert("Server Error. Please try again.");
                }
            })
            .catch((error) => {
                console.log(error);
                alert("Server Error. Please try again.");
            });
    }
}
