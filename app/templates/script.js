// URLs
var registration_url = "http://localhost:8000/api/account/register";
var cust_login_url = "http://localhost:8000/api/customer/customerlogin";
var agent_login_url = "http://localhost:8000/api/agent/agentlogin";
var recommendation_url = "http://localhost:8000/api/reco/getRecPolicies";
var checkout_url = "http://localhost:8000/api/checkout/checkout";
var payment_url = "http://localhost:8000/api/payment/payment";
var view_customers_url = "http://localhost:8000/api/view_agent_custs/viewAgentCusts";
var view_customers_policy_url = "http://localhost:8000/api/customer/viewPolicies";

// Account
async function register(){
    var nric = document.getElementById("nric").value; 
    var pw = document.getElementById("password").value;
    var cpw = document.getElementById("confirmPassword").value;

    if(pw!==cpw){
      alert("Passwords don't match. Please try again.")
      return
    }

    var email = document.getElementById("email").value;

    const data = {
        "cust_nric":nric,
        "cust_password":pw,
        "cust_email":email
    }

    console.log("registering")  

    try{
        const response = await fetch(registration_url,{
            method:'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        console.log(response)

        const result = await response.json();

        console.log(result)
        if(result.code===201){
            localStorage['success_register'] = "yes"; 
            window.location.replace("login.html");
        } 
        else if (result.code === 403) {
            var error_msg = 'NRIC/user has registered before. <a href="login.html" class="alert-link">Login in now</a>'
            error_register(error_msg)
        } else {
            var error_msg = 'Please refresh the page and try again.'
            error_register(error_msg)
        }

    } catch(error) {
        console.log(error)
    }
}

function error_register(error_msg) {
    if (document.getElementById("error_msg")) {
        document.getElementById("error_msg").remove()
    }

    var disclaim_div = document.createElement("DIV")
    var div_class = document.createAttribute("class")
    div_class.value = "alert alert-danger"
    disclaim_div.setAttributeNode(div_class); 
    var div_role = document.createAttribute("role")
    div_role.value = "alert"
    disclaim_div.setAttributeNode(div_role)
    var div_id = document.createAttribute("id")
    div_id.value = "error_msg"
    disclaim_div.setAttributeNode(div_id); 
    disclaim_div.innerHTML = "<i class='fas fa-exclamation-circle'></i> " + error_msg

    form_object = document.getElementById('register_form')
    form_object.prepend(disclaim_div)
}

function check_registration() {
    if (localStorage['success_register']) {
        var success_div = document.createElement("DIV")
        var div_class = document.createAttribute("class")
        div_class.value = "alert alert-success"
        success_div.setAttributeNode(div_class); 
        var div_role = document.createAttribute("role")
        div_role.value = "alert"
        success_div.setAttributeNode(div_role)
        var div_id = document.createAttribute("id")
        div_id.value = "register_success"
        success_div.setAttributeNode(div_id); 
        success_div.innerHTML = "<i class='far fa-check-circle'></i> <b>Registration Successful!</b> Log in now."

        form_object = document.getElementById('login-form')
        form_object.prepend(success_div)

        window.localStorage.removeItem('success_register');
    }
}

async function login() {
    var nric = document.getElementById("nric").value; 
    var pw = document.getElementById("password").value;

    // Check if its agent 
    if (document.forms['login_form']['agent'].checked){
        const data = {
            "agent_nric":nric,
            "agent_password":pw
        };

        console.log(data)
        console.log("logging in")  

        try{
            const response = await fetch(agent_login_url,{
                method:"POST",
                mode: "cors",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            if(result.code === 200){
                console.log(result);
                agent_id = result['data']['agent_id']
                localStorage['agent_name'] = result['data']['agent_name']
                localStorage['agent_id'] = agent_id
                window.location.replace("agent.html");
            }
            else if (result.code === 403 || result.code === 404) {
                if (document.getElementById("error_msg") == null) {
                    if (document.getElementById("register_success")) {
                        document.getElementById("register_success").remove()
                    }

                    var disclaim_div = document.createElement("DIV")
                    var div_class = document.createAttribute("class")
                    div_class.value = "alert alert-danger"
                    disclaim_div.setAttributeNode(div_class); 
                    var div_role = document.createAttribute("role")
                    div_role.value = "alert"
                    disclaim_div.setAttributeNode(div_role)
                    var div_id = document.createAttribute("id")
                    div_id.value = "error_msg"
                    disclaim_div.setAttributeNode(div_id); 
                    disclaim_div.innerHTML = "<i class='fas fa-exclamation-circle'></i> Invalid NRIC or Password"

                    form_object = document.getElementById('login-form')
                    form_object.prepend(disclaim_div)
                }
            }
            console.log(result)

        } catch(error){
            console.log(error);
        }

    }
    else{
        const data = {
            "cust_nric":nric,
            "cust_password":pw
        };
        console.log(data)
        console.log("logging in")  

        try{
            const response = await fetch(cust_login_url,{
                method:"POST",
                mode: "cors",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            if(result.code === 200){
                console.log(result);

                localStorage['nric'] = nric;
                localStorage['cust_name'] = result['data']['cust_name']
                window.location.replace("categories.html");
            }
            else if(result.code === 403 || result.code === 404){
                if (document.getElementById("error_msg") == null) {
                    if (document.getElementById("register_success")) {
                        document.getElementById("register_success").remove()
                    }

                    var disclaim_div = document.createElement("DIV")
                    var div_class = document.createAttribute("class")
                    div_class.value = "alert alert-danger"
                    disclaim_div.setAttributeNode(div_class); 
                    var div_role = document.createAttribute("role")
                    div_role.value = "alert"
                    disclaim_div.setAttributeNode(div_role)
                    var div_id = document.createAttribute("id")
                    div_id.value = "error_msg"
                    disclaim_div.setAttributeNode(div_id); 
                    disclaim_div.innerHTML = "<i class='fas fa-exclamation-circle'></i> Invalid NRIC or Password"

                    form_object = document.getElementById('login-form')
                    form_object.prepend(disclaim_div)
                }
            }
            console.log(result)

        } catch(error) {
            console.log(error);
        }
    }
}

// Recommendation
function storeCategory(category) {
    console.log('storing');
    localStorage['category'] = category;
}

function storePolicy(policy_id, company,premium) {
    console.log('storing');
    localStorage['policy_id'] = policy_id;
    localStorage['company'] = company;
    localStorage["premium"] = premium;
}

function showCategory(){
    var category = localStorage['category'];
    var place = document.getElementById("recpolcat");
    if(category==="critical_illness"){
        place.innerText = "Critical Illness"
    }
    else if(category==="whole_life"){
        place.innerText = "Whole Life"
    }
    else {
        place.innerText = "Savings"
    }
    
}

function displayForm() {
    console.log("displaying");
    var category = localStorage['category'];
    if (category == 'savings') {
        // show the minimum initial deposit
        document.getElementsByClassName('form-title')[0].innerHTML = 'Savings Form';
        var savings = document.getElementsByClassName('savings');
        for(var qn of savings) {
            qn.style.display = 'block';
        }          
        // hide the critical illness and do you smoke qn
        var non_savings = document.getElementsByClassName('non-savings');
        for(var qn of non_savings) {
            qn.style.display = 'none';
        }
    }
    else {
        if (category == 'whole_life') {
            document.getElementsByClassName('form-title')[0].innerHTML = 'Whole Life Form';
        }
        else {
            document.getElementsByClassName('form-title')[0].innerHTML = 'Critical Illness Form';
        }
        // hide the minimum initial deposit
        var savings = document.getElementsByClassName('savings');
        for(var qn of savings) {
            qn.style.display = 'none';
        }        
        // show the critical illness and do you smoke qn
        var non_savings = document.getElementsByClassName('non-savings');
        for(var qn of non_savings) {
            qn.style.display = 'block';
        }
    }
}

async function getRecPolicies(){
    console.log("getting policies");
    var returns = document.forms['recoPolicies']['rateOfReturn'].value;
    var monthly_budget = document.forms['recoPolicies']["monthlyPremium"].value;
    var initial_deposit = document.forms['recoPolicies']["initialDeposit"].value;
    var critical_ill= document.forms['recoPolicies']["criticalIllness"].value;
    var smoke = document.forms['recoPolicies']['smoke'].value;

    // console.log(returns);

    var data = {
        "nric": localStorage['nric'],
        "category": localStorage['category'],
        "returns":  returns,
        "monthly_budget": parseInt(monthly_budget),
        "initial_deposit": parseInt(initial_deposit),
        "critical_ill": critical_ill,
        "smoke": smoke
    };
    try{
        console.log(JSON.stringify(data));
        const response = await fetch(recommendation_url, {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        var result = await response.json();
        if(result.code===200){
            console.log(result);
            localStorage['top_policies'] = JSON.stringify(result.data);
            window.location.replace("policies.html");

        } else if(result.code===400){
            console.log("Invalid JSON input")
        } else {
            console.log(result)
        }
    } catch(error) {
        console.log(error);
    }
}

function displayPolicies() {
    var policies = JSON.parse(localStorage['top_policies'])['recommended_policies'];

    if (policies.length != 0) {
        var categories = localStorage['category'];
        console.log(policies);

        area = document.getElementById("recommended");
        
        display = ''
        
        if(categories == 'critical_illness'){
            for(var i=0; i<policies.length;i++){
                policy = policies[i];
                policyID = policy["policyId"];
                company = policy["company"];
                prem = policy["premium_derived"];

                if (company == 'Aviva') {
                    logo = '<img src="assets/img/aviva.png" style="width:60px;height:60px; margin-bottom: 27px;" alt="aviva-logo">'
                } else if (company == 'AIA') {
                    logo = '<img src="assets/img/aia.png" style="width:90px;height:80px; margin-bottom: 17px;" alt="aia-logo">'
                } else {
                    logo = '<img src="assets/img/great-eastern.png" style="width:90px;height:90px;" alt="great-eastern-logo"></img>'
                }

                display+=`
                <div class="col-md-6 col-lg-4 justify-content-center flex-wrap" data-aos="zoom-in"
                data-aos-delay="100">
                <a href='payment.html' onclick="storePolicy('${policyID}','${company}','${prem}')">
                <div class="icon-box mx-auto">
                    ${logo}
                    <h6 class="title ml-0" style="text-align:left;"><span style='color: black;'>Category:</span> ${policy['category']}</h6>
                    <h6 class="title ml-0" style="text-align:left;"><span style='color: black;'>Company:</span> ${policy['company']}</h6>
                    <h6 class="title ml-0" style="text-align:left;"><span style='color: black;'>Policy ID:</span> ${policy['policyId']}</h6>
                    <h6 class="title ml-0" style="text-align:left;"><span style='color: black;'>Name:</span> ${policy['name']}</h6>
                    <hr style='mb-2'>
                    <h6 class="title ml-0" style="text-align:left;"><span style='color: black;'>Monthly Premium:</span> ${currencyFormat(policy['premium_derived'])}</h6>
                    <h6 class="title ml-0" style="text-align:left;"><span style='color: black;'>Conditions Covered:</span> ${policy['num_condition_covered']}</h6>
                    <h6 class="title ml-0" style="text-align:left;"><span style='color: black;'>Sum Insured:</span> ${currencyFormat(policy['sum_insured'])}</h6>
                </div>
                </a>
                </div>`;
            }
        }
        else{
            for(var i=0; i<policies.length;i++){
                policy = policies[i];
                policyID = policy["policyId"];
                company = policy["company"];
                prem = policy["monthly_premium"];

                if (company == 'Aviva') {
                    logo = '<img src="assets/img/aviva.png" style="width:60px;height:60px; margin-bottom: 27px;" alt="aviva-logo">'
                } else if (company == 'AIA') {
                    logo = '<img src="assets/img/aia.png" style="width:90px;height:80px; margin-bottom: 17px;" alt="aia-logo">'
                } else {
                    logo = '<img src="assets/img/great-eastern.png" style="width:90px;height:90px;" alt="great-eastern-logo"></img>'
                }

                benefits = ''

                if(categories == 'whole_life') {
                    benefits = `
                    <h6 class="title ml-0" style="text-align:left;"><span style='color: black;'>Coverage:</span> ${policy['coverage'].join(", ")}</h6>
                    <h6 class="title ml-0" style="text-align:left;"><span style='color: black;'>Sum Insured:</span> ${currencyFormat(policy['sum_insured'])}</h6>`
                } else {
                    benefits = `
                    <h6 class="title ml-0" style="text-align:left;"><span style='color: black;'>Initial Deposit:</span> ${currencyFormat(policy['initial_deposit'])}</h6>
                    <h6 class="title ml-0" style="text-align:left;"><span style='color: black;'>Rate of Return:</span> ${policy['rate_of_return_per_annum']}%</h6>`
                }

                display+=`
                <div class="col-md-6 col-lg-4 justify-content-center flex-wrap" data-aos="zoom-in"
                data-aos-delay="100">
                <a href='payment.html' onclick="storePolicy('${policyID}','${company}','${prem}')">
                <div class="icon-box mx-auto">
                    ${logo}
                    <h6 class="title ml-0" style="text-align:left;"><span style='color: black;'>Category:</span> ${policy['category']}</h6>
                    <h6 class="title ml-0" style="text-align:left;"><span style='color: black;'>Company:</span> ${policy['company']}</h6>
                    <h6 class="title ml-0" style="text-align:left;"><span style='color: black;'>Policy ID:</span> ${policy['policyId']}</h6>
                    <h6 class="title ml-0" style="text-align:left;"><span style='color: black;'>Name:</span> ${policy['name']}</h6>
                    <hr style='mb-2'>
                    <h6 class="title ml-0" style="text-align:left;"><span style='color: black;'>Monthly Premium:</span> ${currencyFormat(policy['monthly_premium'])}</h6>
                    ${benefits}
                </div>
                </a>
                </div>`;
            }
            
        }

        area.innerHTML = display; 
    }
    
    else {
        document.getElementById("header_reco").innerHTML = `<br><i class="far fa-frown-open"></i> <br>Sorry.. No suitable policies due exceeded age limit.`;
    }
}

function currencyFormat(num) {
    return '$' + num.toFixed(2).replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')
}

// Checkout
async function checkout() {
    console.log("checking out");
    var nric = localStorage['nric'];
    var company = localStorage['company'];
    var policy_id = localStorage['policy_id'];
    var premium = localStorage["premium"];
    var url = checkout_url + '/' + nric + '/' + company + '/' + policy_id + '/' + premium;
    console.log(url);
    try{
        const response = await fetch(url, {
            method: "GET",
            mode: 'cors'
        });
        var result = await response.json();
        
        if(result.code==200){
            console.log("success");
            console.log(result);
            var information = result.data;

            localStorage["customer_name"] = information["customer_name"];
            localStorage["email"] = information["email"];
            localStorage["policy_name"] = information["policy_name"];
            localStorage["policy_price"] = information["policy_price"];

            var title = document.getElementById("title");
            title.innerHTML = information["policy_name"];

            var loading_spinner = document.getElementById("loading_spinner");
            loading_spinner.remove();

            if (localStorage['category'] == 'whole_life') {
                formatted_cat = 'Whole Life'
            } else if (localStorage['category'] == 'savings') {
                formatted_cat = 'Savings'
            } else {
                formatted_cat = 'Critical Illness'
            }

            document.getElementById("summary_checkout").innerHTML += `<div class="row mb-2">
                <div class="col text-center">
                    <h4 class="sum-header-company">Company</h4>
                </div>
                <div class="col text-center">
                    <h4 class="sum-header-id">Policy ID</h4>
                </div>
                <div class="col text-center">
                    <h4 class="sum-header-cat">Category</h4>
                </div>
                <div class="col text-center">
                    <h4 class="sum-header-price">Monthly Premium</h4>
                </div>
            </div>

            <div class="row font-weight-bold">
                <div class="col text-center" id="company">${localStorage["company"]}</div>
                <div class="col text-center" id="polID">${information["policy_id"]}</div>
                <div class="col text-center" id="category">${formatted_cat}</div>
                <div class="col text-center" id="price">${currencyFormat(Number(information["policy_price"]))}</div>
            </div>`;

            document.getElementById("outer_summary").innerHTML += `<div class="form-group mt-5 mb-0">
                <div class="text-center">
                    <button type="submit" class="btn btn-primary"
                        onclick="add_loading(); makePayment();">Make payment by PayPal</button>
                </div>
            </div>`;

            localStorage['summary'] = JSON.stringify(response.data);

        }else if(response.code==400){
            console.log(result)
        } 
    } catch(error) {
        console.log(error);
    }
}



// Payment
async function makePayment() {
    console.log("clicked");

    var data = {
        "nric": localStorage['nric'],
        "policy_id": localStorage['policy_id'],
        "policy_name": localStorage["policy_name"],
        "policy_price": localStorage["policy_price"],
        "cust_name": localStorage["customer_name"],
        "email": localStorage["email"]
    }
    console.log(data)
    try{
        const response = await fetch(payment_url,{
            method:"POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        const result = await response.json();
        console.log(result);
        window.location.href = result['approval_URL'];
    } catch(error){
        console.log(error);
    }
}

function add_loading() {
    document.getElementById("summary").innerHTML = `<div class="text-center" style='margin-top: 50px'>
        <div class="spinner-border text-warning" role="status" style="width: 7rem; height: 7rem;">
            <span class="visually-hidden"></span>
        </div>
    </div>`;
}


// View Customers
async function viewCustomers() {
    
    var agent_id = localStorage['agent_id'];
    var data = {
        "agent_id": agent_id
    }
    area = document.getElementById("customers_viewer");
    console.log(data);
    try{
        const response = await fetch(view_customers_url +"/" + data['agent_id'], {
            method:"GET",
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        const result = await response.json();
        if(result.code===200){
            console.log(result);
            document.getElementById('header_cust').innerText = "Here are the customers that you manage";

            var cust_list = result['data']['cust_list']
            var count = 1
            var display = ''
            console.log(cust_list);
            for(let cust of cust_list){
                var cust_name = cust['cust_name'];
                var cust_nric = cust['cust_nric'];
                
                var cust_phone_number = cust['mobile_no'];
                var cust_dob = cust['cust_dob'];
                var email = cust['cust_email'];

                display += `<tr class="text-center hover-row" onclick="saveCustomerDetails('${cust_nric}', '${cust_name}')">
                                <td>${count}</td>
                                <td>${cust_name}</td>
                                <td>${cust_nric}</td>
                                <td>${cust_phone_number}</td>
                                <td>${cust_dob}</td>
                                <td>${email}</td>
                             </tr>
                `;
                count++;
            }

            area.innerHTML = area.innerHTML + display;
      
        }else if(result.code===404){
            console.log(result.message)
            document.getElementById('tablecust').innerHTML = "<h2>No customers assigned to you yet!</h2>";
        }       

    } catch(error){
        console.log(error);
    }
}

// logout
function logout() {
    window.localStorage.clear();
    window.location.href = 'index.html'
}

// Check localstorage variables
function check_localstorage() {
    var values = {},
    keys = Object.keys(localStorage),
    i = keys.length;

    while ( i-- ) {
        values[keys[i]] = localStorage.getItem(keys[i])
    }

    console.log(values)
}


async function saveCustomerDetails(cust_nric, cust_name){
    window.location='view-customer.html';
    localStorage['cust_nric_chosen'] = cust_nric;
    localStorage['cust_name_chosen'] = cust_name;
    
}
async function viewCustomerPolicies(){

    var cust_nric = localStorage['cust_nric_chosen'] ;
    var cust_name = localStorage['cust_name_chosen'];
    // console.log(cust_name);
    var data = {
        "cust_nric": cust_nric
    }
    area = document.getElementById("policyViewer");
    var addCustNameArea = document.getElementById("addCustName")
    console.log(data);
    
    try{
        const response = await fetch(view_customers_policy_url +"/" + data['cust_nric'], {
            method:'GET',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        const result = await response.json();
        if(result.code===200){
            console.log(result);
            var policy_list = result['data'];
            var count = 1
            console.log(policy_list);
            var display = ''
            // console.log(cust_list);
            for(let policy of policy_list){
                var category = policy['policy_category'];
                var policy_name = policy['policy_name'];
                var policy_id = policy['policy_id'];
                var price = policy['monthly_premium'];

                display += `<tr class="text-center" class="clickable text-center">
                                <td>${count}</td>
                                <td>${category}</td>
                                <td>${policy_name}</td>
                                <td>${policy_id}</td>
                                <td>${currencyFormat(Number(price))}</td>
                             </tr>
                `;
                count++;
            }

            area.innerHTML = area.innerHTML + display;
            addCustNameArea.innerHTML += `<p>Policies under ${cust_name}</p>`;
        }else if(result.code===404){
            console.log(result.message)
            document.getElementById('outer_table').innerHTML = "<h2>Customer did not buy any policy yet..</h2>";
        }       

    } catch(error){
        console.log(error);
    }
}