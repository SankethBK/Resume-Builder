
    var name,phone, email, linkedin, skills, degree, field, graduationYear, university, highSchool, projects, workExperience, achievements;
    var previewBtn = document.getElementById('preview');
    var form = document.getElementsByTagName('form')[0];
    var backBtn = document.getElementById('back');
    var finish = document.getElementById('finish');
    previewBtn.addEventListener('click' , function(){
        preview.style.display = "none";
        form.style.display = "none";
        backBtn.style.display = "";
        takeInput();
        print();
        var img = myCanvas.toDataURL('image/png');
        var canvasImg = document.getElementById("targetImage");
        canvasImg.setAttribute('src',img);
    }); 
    backBtn.addEventListener('click' , function(){
        myCanvas.style.display = "none";
        var canvasImg = document.getElementById("targetImage");
        canvasImg.setAttribute('src',"");
        backBtn.style.display = "none";
        form.style.display = "";
        preview.style.display = "";
    });
    finish.addEventListener('click' , function() {
        takeInput();
        print();
        localStorage.setItem('resumels', myCanvas.toDataURL());

    });
    function removeSpace(text){
        let i = 0;
        while (text[i] == ' '){
            i += 1;
        }
        return text.slice(i);
    }

    function takeInput(){
        name = document.getElementById('name').value;
        phone = document.getElementById('phone').value;
        email = document.getElementById('email').value;
        linkedin = document.getElementById('linkedin').value;
        skills = document.getElementById('skills').value;
        degree = document.getElementById('degree').value;
        field = document.getElementById('field').value;
        graduationYear = document.getElementById('gradyear').value;
        highSchool = document.getElementById('highschool').value
        university = document.getElementById('university').value;
        projects = document.getElementById('projects').value;
        professionalSummary = document.getElementById('professionalsummary').value;
        workExperience = document.getElementById('workexperience').value; 
        achievements = document.getElementById('achievements').value;       
    }

    function preProcessAndPaste(text , numChars){
        var wordList = [];
        var start = 0;
        var end = numChars;
        if (!text){
            return wordList;
        }
        while (true){
            if (end  >= text.length){
                wordList.push(text.slice(start,));
                return wordList;
            }
            wordList.push(removeSpace(text.slice(start,end)));
            start = end; 
            end += numChars;
        }
    
        return wordList;
    }

    var myCanvas = document.querySelector("#myCanvas");
    var ctx = myCanvas.getContext("2d"); 


    function drawBullet(x, y, r){
        ctx.beginPath();
        ctx.arc(x, y, r, 0, 2 * Math.PI);
        ctx.fill();            
    }

    
    function properPaste(textList, bullet, startX, startY, textColor, numChars, lineGap){
        ctx.fillStyle = textColor;
        for (var i = 0; i < textList.length ; ++i){
            textList[i] = preProcessAndPaste(textList[i], numChars);
        }

        x = startX;
        y = startY;
        for (var i = 0; i < textList.length ; ++i){
            if (bullet){
                drawBullet(x + 5, y - 4 , bullet);
                x += 10;
            }

            for (var j = 0; j < textList[i].length; ++j){
                ctx.fillText(textList[i][j], x, y);
                x = startX;
                y += lineGap;
            }
        }
        
    }
    function setBold(color){
        ctx.fillStyle = color;
        ctx.font = "bold 30px  Arial";
    }
    function setNormal(color){
        ctx.fillStyle = color;
        ctx.font = "18px Arial";
    }

    function print(){

        
        ctx.clearRect(0,0,myCanvas.width, myCanvas.height);
        ctx.fillStyle = 'white';
        ctx.fillRect(240,0, myCanvas.getAttribute('width') , myCanvas.getAttribute('height'));
        ctx.fillStyle = "#8a6b38";
        ctx.fillRect(0,0, 240,195);
        ctx.fillStyle = "#bf9771";
        ctx.fillRect(0,195,240,myCanvas.getAttribute('height')-195);
        ctx.fillRect(240,0,myCanvas.getAttribute('width')-240,195);
        ctx.fillStyle = 'black';
        ctx.font = 'bold 35px Arial';
        var y = 50;
        if (name.length > 10){
            console.log("name's langth is ",name.length);
            properPaste([name], false, 10, y, 'black', 11, 30);
            y += 60;
        }
        else{
            ctx.fillText(name, 10, y);
            y += 30;
        }

        setNormal('black');
        properPaste([email, phone, linkedin] ,0, 10, y, 'black', 25, 20);
        y += 139;
        
        setBold('black');
        ctx.fillText("Skills", 10, y);
        y += 32;
        setNormal('black');
        properPaste(skills.split(','), 3, 10, y, 'black', 25, 19);
        y += 210;
        setBold('black');
        ctx.fillText("Education", 10, y);

        var deg = "studied " + degree + " in " + field + " from " + university + " ," + graduationYear;

        setNormal('black');
        var hs = "";
        hs = "completed high school education from " + highSchool;
        y += 40;
        properPaste([deg, hs], false, 10, y, 'black', 21 , 19);

        y = 35;
        setBold('black');
        ctx.fillText('Professional Summary', 245, y)
        setNormal('black');
        y += 35;
        properPaste([professionalSummary], false, 248, y, 'black', 55, 19);
        y += 150;
        setBold("black");
        ctx.fillText("Projects", 248, y);
        setNormal('black');
        y += 35;
        properPaste(projects.split('\n'), 3, 248, y, 'black', 55, 19);

        y += 130;
        setBold('black');
        ctx.fillText("Work Experience", 248, y);
        setNormal('black');
        y += 30;
        properPaste(workExperience.split('\n'),3, 248, y, 'black', 55, 19)
        
        y += 140;
        setBold('black');
        ctx.fillText('Achiements', 248, y);
        setNormal('black');
        y += 30;
        properPaste(achievements.split('\n'), 3, 248, y, 'black', 55, 19);
    }
   
