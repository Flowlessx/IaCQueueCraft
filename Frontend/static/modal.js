document.addEventListener("DOMContentLoaded", function() {
    // Modal logic
    var modal = document.getElementById("myModal");
    var show_modal = document.getElementById("show_modal").value;
    if (show_modal === "True") {
        modal.style.display = "block";
    }
    var span = document.getElementsByClassName("close")[0];
    span.onclick = function() {
        modal.style.display = "none";
    }
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // Event listeners for buttons
    document.getElementById('register_company').addEventListener('click', function() {
        const companyName = document.getElementById('name').value;
        if (companyName) {
            fetch('/register_company', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({'name': companyName})
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
                alert(data.message);
            })
            .catch(error => console.error('Error:', error));
        } else {
            alert('Please enter the company name');
        }
    });

    document.getElementById('get_companies').addEventListener('click', function() {
        fetch('/get_companies')
        .then(response => response.json())
        .then(data => {
            console.log(data);            
            // Logic to update the company list
            const companyDropdown = document.getElementById('company_cloud_account_create');
            const companyDropdown2 = document.getElementById('company_cloud_account_list');
            
            companyDropdown.innerHTML = ""; // Clear existing options
            companyDropdown2.innerHTML = ""; // Clear existing options
            data.message.forEach(company => {
                const option = document.createElement('option');
                option.value = company.id;
                option.textContent = company.name; 
                companyDropdown.appendChild(option);                
            });
            data.message.forEach(company => {
                const option2 = document.createElement('option');
                option2.value = company.id;
                option2.textContent = company.name; 
                companyDropdown2.appendChild(option2);                
            });            
        })
        .catch(error => console.error('Error:', error));
    });

    document.getElementById('create_account').addEventListener('click', function() {
        const company = document.getElementById('company_cloud_account_create').value;
        const platform = document.getElementById('account_platform').value;
        const accountName = document.getElementById('account').value;
        const accountType = document.getElementById('account_type').value;
        if (company && platform && accountName && accountType) {
            fetch('/create_account', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({                   
                    'company_id': company,
                    'platform': platform,
                    'account_name': accountName,
                    'account_type': accountType
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
                alert(data.message);
            })
            .catch(error => console.error('Error:', error));
        } else {
            alert('Please fill in all fields');
        }
    });

    document.getElementById('get_account').addEventListener('click', function() {
        const company = document.getElementById('company_cloud_account_list').value;
        if (company) {
            fetch('/get_accounts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({'company_id': company})
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);               
                populateAwsAccountsTable(data.message);
            })
            .catch(error => console.error('Error:', error));
        } else {
            alert('Please select a company');
        }
    });
    function populateAwsAccountsTable(accounts) {
        const tableBody = document.getElementById('aws_accounts_table').getElementsByTagName('tbody')[0];
        tableBody.innerHTML = ''; // Clear existing rows
    
        accounts.forEach(account => {
            const row = tableBody.insertRow();
            const cellID = row.insertCell(0);
            const cellName = row.insertCell(1);
            const cellCompanyID = row.insertCell(2);
    
            cellID.textContent = account.id;
            cellName.textContent = account.name;
            cellCompanyID.textContent = account.company_id;
        });
    }
    document.getElementById('company_account').addEventListener('change', function() {
        const account = this.value;
        if (account) {
            fetch('/get_account_resources', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({'account': account})
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                // Logic to populate the account resources table
            })
            .catch(error => console.error('Error:', error));
        }
    });
});
