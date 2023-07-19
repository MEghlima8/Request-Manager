var app_methods = {};

app_methods.change_panel = function(target){
    this.panel = target;
}

// Signin
app_methods.signIn = function(){
    var data = {
        'username':this.username,
        'password':this.password,
    }    
    axios.post('/signin', data).then(response => {  
        if (response.data['status-code'] == 200) { 
            //  Login was succesful
            //  Retrieve dashboard info. Count : images and audios and add calc
            axios.post('/res-add-calc').then(response => {this.all_add_requests = response.data["count"]})        
            axios.post('/get-all-audio-steg-req').then(response => {this.all_audio_requests = response.data["count"]})
            axios.post('/get-all-img-steg-req').then(response => {this.all_img_requests = response.data["count"]})
            
            axios.post('/get-user-requests-status').then(response => {
                console.log(response.data)
                this.processing_requests = response.data["processing"]  // count of processing
                this.inQueue_requests = response.data["in queue"]     // count of queue
                this.completed_requests = response.data["done"]   // count of done
                this.all_requests = response.data["done"] + response.data["in queue"] + response.data["processing"]
            })
            this.panel= 'dashboard';
        }        
        else {            
            //  Login was not succesful
            if (response.data['status-code'] == 'False'){alert('نام کاربری یا رمز عبور اشتباه است')}
            else if (response.data['status-code'] == 403){alert('این ایمیل هنوز تایید نشده است.برای تایید به ایمیل خود بروید و روی لینک تایید کلیک کنید ')}
            else if (response.data['status-code'] == 401){alert('نام کاربری یا رمز عبور معتبر نیست')}
            else { alert('اطلاعات نامعتبر هستند') }
            this.panel = 'sign-in'
        }
    })
}

// Signup
app_methods.signUp = function(){
    var data = {
        'username' : this.username,
        'password' : this.password,
        'email' : this.email,
    }    
    axios.post('/signup', data).then(response => {  
        if (response.data['status-code'] == 201) { 
            //  Signup was succesful
            this.panel= 'sign-in';
            alert('ثبت نام با موفقیت انجام شد. لینک تایید به ایمیل شما ارسال شد.');
        }        
        else if (response.data['result'] == 'duplicate_username' ) { alert("نام کاربری وارد شده در سیستم وجود دارد."); }
        else if (response.data['result'] == 'duplicate_email') {alert('ایمیل وارد شده در سیستم وجود دارد.')}
        else if (response.data['result'] == 'noactive') {alert('لطفا بر روی لینک تایید شده به ایمیل تان بزنید. ')}
        else if (response.data['result'] == 'char_password') {alert('رمز عبور باید شامل حروف کوچک و بزرگ انگلیسی اعداد و کاراکتر های خاص باشد')}
        else{ alert('فرمت اطلاعات وارد شده اشتباه است') }
    })
}


// Add calc
app_methods.resAddCalc = function(){
    axios.post('/get-all-add-req').then(response => {          
        this.res_queue = response.data["queue"]
        this.res_processing = response.data["processing"]
        this.res_done = response.data["done"]  
    })
    this.change_panel('res-add-calc');
}

app_methods.sendAddCalcReq = function(){
    data = {
        "params": {
            "num1": parseInt(this.CalcNum1),
            "num2": parseInt(this.CalcNum2)
        }
    }
    
    if (typeof data["params"]["num2"] !== 'number' || typeof data["params"]["num2"] !== 'number' || isNaN(data["params"]["num1"]) || isNaN(data["params"]["num2"]) || data["params"]["num1"] === '' || data["params"]["num2"] === '') {
        alert('مقادیر وارد شده باید عدد باشند و نباید خالی باشند.');
      }
    else {
        axios.post('/add', data).then(response => {  
            alert('درخواست شما تایید شد.')
        })}
}
// # Add calc


//  steg image 
app_methods.resStegImg = function(){
    axios.post('/get-all-img-res').then(response => {          
        this.res_queue = response.data["queue"]
        this.res_processing = response.data["processing"]
        this.res_done = response.data["done"]
    })
    this.change_panel('res-steg-img')    
}
app_methods.handleStegNewReqImg = function(event){
    this.img_steg_new_req_img = event.target.files[0]
}

app_methods.stegNewReqImg = function(){
    
    if (this.msg_steg_newreq_img === '' || this.img_steg_new_req_img === '') {
        alert('لطفاً مقادیر را پر کنید و یا فایل را آپلود کنید.');
        return ;
    }
    if (this.img_steg_new_req_img.type.startsWith('image/')) {
        const fd = new FormData();
        fd.append('img_steg_new_req_img',this.img_steg_new_req_img)
        fd.append('msg_steg_newreq_img', this.msg_steg_newreq_img)
        axios.post('/hide-text', fd).then(response => { 
            alert('درخواست شما تایید شد.')
            })
    }
    else {alert('فرمت فایل معتبر نیست.')}
}
// # steg image 


// Extract steg image
app_methods.resExtrStegImg = function(){
    axios.post('/res-extr-steg-img').then(response => {          
        this.res_queue = response.data["queue"]
        this.res_processing = response.data["processing"]
        this.res_done = response.data["done"]
        this.change_panel('res-extr-steg-img')
    })
}

app_methods.handleExtrStegNewImg = function(event){
    this.extr_steg_img = event.target.files[0]
}

app_methods.extrStegImg = function(){

    if (this.extr_steg_img === '' ) {
        alert('لطفاً مقادیر را پر کنید و یا فایل را آپلود کنید.');
        return ;
    }
    if (this.extr_steg_img.type.startsWith('image/')) {
        const fd = new FormData();
        fd.append('extr_steg_img',this.extr_steg_img)
    
        axios.post('/get-text', fd).then(response => { 
            alert('درخواست شما تایید شد.')
               })
    }
    else {alert('فرمت فایل معتبر نیست.')}
}


// # Extract steg image


// Extract steg audio
app_methods.handleExtrNewAudio = function(event){
    this.extr_steg_audio = event.target.files[0]    
}

app_methods.extrNewReqAudio = function(){

    if (this.extr_steg_audio === '' ) {
        alert('لطفاً فایل را آپلود کنید.');
        return ;
    }
    if (this.extr_steg_audio.type.startsWith('audio/')) {
        const fd = new FormData();
        fd.append('extr_steg_audio',this.extr_steg_audio)
        axios.post('/get-from-sound', fd).then(response => { 
            alert('درخواست شما تایید شد.')
            })
    }
    else {alert('فرمت فایل معتبر نیست.')}

}

app_methods.resExtrStegAudio = function(){
    axios.post('/res-extr-steg-audio').then(response => {          
        this.res_queue = response.data["queue"]
        this.res_processing = response.data["processing"]
        this.res_done = response.data["done"]
        this.change_panel('res-extr-audio')
    })
}
// # Extract steg audio


// # Steg audio
app_methods.resStegAudio = function(){
    axios.post('/res-steg-audio').then(response => {          
        this.res_queue = response.data["queue"]
        this.res_processing = response.data["processing"]
        this.res_done = response.data["done"]
        this.change_panel('res-steg-audio')
    })
}

app_methods.handleNewReqAudio = function(event){
    this.audio_newreq_audio = event.target.files[0]
}

app_methods.steg_new_req_audio = function(){

    if (this.audio_newreq_audio === '' || this.msg_newreq_audio === '') {
        alert('لطفاً مقادیر را پر کنید و یا فایل را آپلود کنید.');
        return ;
    }
    if (this.audio_newreq_audio.type.startsWith('audio/')) {
        const fd = new FormData();
        fd.append('msg_newreq_audio',this.msg_newreq_audio)
        fd.append('audio_newreq_audio',this.audio_newreq_audio)
        axios.post('/hide-in-sound', fd).then(response => { 
            alert('درخواست شما تایید شد.')
            })
    }
    else {alert('فرمت فایل معتبر نیست.')}


}
// # Steg audio



Vue.createApp({

    data(){ return {
        // all_panels :['add-calc' , 'res-add-calc' ,
        //             'extr-newreq-steg-audio' ,'res-extr-audio' , 'res-steg-audio' , 'steg-newreq-audio' ,
        //             'extr-newreq-steg' , 'res-extr-steg-img' , 'res-steg-img' , 'steg-newreq-img',
        //             'sign-in' , 'sign-up' ,
        //             'dashboard' ],
        
        panel: 'sign-in',
        
        // add-calc
        CalcNum1: '',
        CalcNum2: '',

        // steg newreq audio
        msg_newreq_audio: '',
        audio_newreq_audio : '',

        // steg-newreq-img
        msg_steg_newreq_img:'',
        img_steg_new_req_img: '',

        // extract steg image 
        extr_steg_img:'',

        // extract new req audio
        extr_steg_audio:'',

        // result for all pages
        res_done: '',
        res_processing : '',
        res_queue: '',

        //  SignIn Info
        username: '',
        password: '',
        //  SignUp Info
        email:'',

        // Dashboard info
        all_requests: 0,
        completed_requests: 0 ,
        processing_requests: 0 ,
        inQueue_requests : 0,
        all_add_requests: 0,
        all_audio_requests: 0,
        all_img_requests: 0,
    } },
    
    delimiters: ["${", "}$"],    
    methods:app_methods,
    
}).mount('#app')