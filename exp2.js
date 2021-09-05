var express=require("express");
var app=express();
var studentroutes=require("./student.routes")
var employeeroutes=require("./employee.routes")

app.use(express.urlencoded({extended:true}))
app.use(express.json());
app.set('view engine', 'pug');
app.set('views','./views');


app.get("/",function(req,res){
    res.sendFile(__dirname+"/home.html")
})

app.use("/student",studentroutes)

app.use("/employee",employeeroutes)

app.listen(8090,function(){
    console.log("listening on 8090")
})