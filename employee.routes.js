var express=require("express");
var router=express.Router();
var employees=[];

router.get("/regemployee",function(req,res){
    res.sendFile(__dirname+"/registeremployee.html");
})

router.get("/emplist",function(req,res){
    res.render("employees",{
        allstudents:employees
    })
})

router.post("/empregister",function(req,res){
    employees.push(req.body);
    res.send("employee regitration succesfull")
})

module.exports=router;
