let seconds = 0;

let timer;

let currentSubject = "";

let studyData = {};

window.onload = function(){

    let savedSubjects = JSON.parse(

        localStorage.getItem("subjects")

    );

    let dropdown = document.getElementById(
        "subject"
    );

    if(savedSubjects){

        savedSubjects.forEach(function(sub){

            let option =
            document.createElement("option");

            option.text = sub;

            option.value = sub;

            dropdown.appendChild(option);
        });
    }
}

function startStudy(){

    currentSubject =
    document.getElementById("subject").value;

    document.getElementById(
        "currentSubject"
    ).innerHTML =

    "📖 Studying: " + currentSubject;

    timer = setInterval(function(){

        seconds++;

        let hrs = Math.floor(seconds / 3600);

        let mins = Math.floor(
            (seconds % 3600) / 60
        );

        let secs = seconds % 60;

        document.getElementById(
            "timer"
        ).innerHTML =

        String(hrs).padStart(2,'0')
        + ":" +

        String(mins).padStart(2,'0')
        + ":" +

        String(secs).padStart(2,'0');

    },1000);
}

function endStudy(){

    clearInterval(timer);

    let totalMinutes =
    Math.floor(seconds / 60);

    if(studyData[currentSubject]){

        studyData[currentSubject]
        += totalMinutes;

    } else {

        studyData[currentSubject]
        = totalMinutes;
    }

    showReport();

    aiRecommendation();

    alert(

        "✅ " +

        currentSubject +

        " Studied for " +

        totalMinutes +

        " Minutes"
    );

    seconds = 0;

    document.getElementById(
        "timer"
    ).innerHTML = "00:00:00";
}

function showReport(){

    let reportHTML = "";

    for(let subject in studyData){

        reportHTML +=

        "<div class='box'>" +

        "<h3>📚 " +
        subject +
        "</h3>" +

        "<p>⏰ " +

        studyData[subject] +

        " Minutes</p>" +

        "</div>";
    }

    document.getElementById(
        "report"
    ).innerHTML = reportHTML;
}

function aiRecommendation(){

    let weakSubject = "";

    let minimumTime = Infinity;

    for(let subject in studyData){

        if(studyData[subject]
            < minimumTime){

            minimumTime =
            studyData[subject];

            weakSubject = subject;
        }
    }

    if(weakSubject !== ""){

        document.getElementById(
            "recommendation"
        ).innerHTML =

        "<div class='box'>" +

        "<h3>⚠ Weak Subject Detected</h3>" +

        "<p>📚 " +

        weakSubject +

        "</p>" +

        "<p>💡 Recommendation: " +

        "Study 30 more minutes today." +

        "</p>" +

        "</div>";
    }
}