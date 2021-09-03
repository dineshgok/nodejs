var fs=require('fs');
fs.readFile("dum1.txt",(err,data)=>{
    console.log(data.toString())
});
console.log("last line")