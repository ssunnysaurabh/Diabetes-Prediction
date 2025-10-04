const mongoose=require('mongoose')

const PeopleSchema=mongoose.Schema({
    name:String,
    email:String,
    password:String
})

const PeopleModel=mongoose.model('people',PeopleSchema)
module.exports=PeopleModel