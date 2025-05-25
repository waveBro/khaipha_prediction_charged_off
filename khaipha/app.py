from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import numpy as np
import joblib
# Import the model
import lightgbm
from sklearn.preprocessing import StandardScaler



app = Flask(
    "app",
    template_folder='c:/Users/vanphuc computer/VietLe-beef/khaipha/src',
    static_folder='c:/Users/vanphuc computer/VietLe-beef/khaipha/src',
    static_url_path='/src'
)

# load model
model = joblib.load('c:/Users/vanphuc computer/VietLe-beef/khaipha/model_info/model.pkl')
scaler  = joblib.load('c:/Users/vanphuc computer/VietLe-beef/khaipha/model_info/scaler.pkl')
threshold = joblib.load('c:/Users/vanphuc computer/VietLe-beef/khaipha/model_info/threshold.pkl')
model2 = joblib.load('c:/Users/vanphuc computer/VietLe-beef/khaipha/model_info2/lgb_model.pkl')
threshold2 = joblib.load('c:/Users/vanphuc computer/VietLe-beef/khaipha/model_info2/threshold.pkl')

@app.route('/')
def index():
    # redict to /kiemtrano
    return redirect(url_for('kiemtrano2_page'))


@app.route("/kiemtrano")
def kiemtrano_page():
    return render_template('page.html')

#api get data from FE
@app.route('/api/kiem_tra_no', methods=['POST'])
def kiemtrano():
    # get data from get_data.js (method: POST)
    data = request.get_json()
    """
    'loan_amnt',
    'annual_inc',
    'dti',
    'bc_open_to_buy',
    'revol_bal',
    'fico',
    'mo_sin_old_rev_tl_op',
    'total_acc',
    'acc_open_past_24mths',
    'tot_cur_bal',
    'earliest_cr_line',
    'num_actv_bc_tl',
    'mths_since_recent_bc',
    'revol_util',
    'num_tl_op_past_12m',
    'delinq_2yrs',
    'mort_acc',
    'mths_since_recent_inq',
    'term_36',
    'application_type_Individual',
    'inq_last_6mths',
    'verification_status_Verified',
    'num_rev_accts',
    'verification_status_Source Verified',
    'pct_tl_nvr_dlq',
    'mo_sin_rcnt_tl',
    'purpose_small_business',
    'NY',
    'purpose_credit_card',
    'MORTGAGE'
    """
    loan_amnt = data['loan_amnt']
    annual_inc = data['annual_inc']
    dti = data['dti']
    bc_open_to_buy = data['bc_open_to_buy']
    revol_bal = data['revol_bal']
    fico = data['fico']
    mo_sin_old_rev_tl_op = data['mo_sin_old_rev_tl_op']
    total_acc = data['total_acc']
    acc_open_past_24mths = data['acc_open_past_24mths']
    tot_cur_bal = data['tot_cur_bal']
    earliest_cr_line = data['earliest_cr_line']
    num_actv_bc_tl = data['num_actv_bc_tl']
    mths_since_recent_bc = data['mths_since_recent_bc']
    revol_util = data['revol_util']
    num_tl_op_past_12m = data['num_tl_op_past_12m']
    delinq_2yrs = data['delinq_2yrs']
    mort_acc = data['mort_acc']
    mths_since_recent_inq = data['mths_since_recent_inq']
    
    term_36 = data['term']
    application_type_Individual = data['application_type']
    
    inq_last_6mths = data['inq_last_6mths']
    
    verification_status_Verified = data['verification_status']
    
    num_rev_accts = data['num_rev_accts']
    
    verification_status_Source_Verified = data['verification_status']
    
    pct_tl_nvr_dlq = data['pct_tl_nvr_dlq']
    mo_sin_rcnt_tl = data['mo_sin_rcnt_tl']
    
    purpose_small_business = data['loan_purpose']
    NY = data['state']
    purpose_credit_card = data['loan_purpose']
    MORTGAGE = data['home_ownership']

    # Check if all required fields are present
    # check application_type
    if application_type_Individual == 'Individual':
        application_type_Individual = 1
    else:
        application_type_Individual = 0

    # check NY
    if NY == 'NY':
        NY = 1
    else:
        NY = 0
    
    # check purpose_small_business
    if purpose_small_business == 'small_business':
        purpose_small_business = 1
    else:
        purpose_small_business = 0
    
    # check purpose_credit_card
    if purpose_credit_card == 'credit_card':
        purpose_credit_card = 1
    else:
        purpose_credit_card = 0
    
    #check term_36
    if term_36 == '36':
        term_36 = 1
    else:
        term_36 = 0

    # check verification_status_Verified
    if verification_status_Verified == 'Verified':
        verification_status_Verified = 1
    else:
        verification_status_Verified = 0

    # check verification_status_Source_Verified
    if verification_status_Source_Verified == 'Source Verified':
        verification_status_Source_Verified = 1
    else:
        verification_status_Source_Verified = 0

    # check home_ownership
    if MORTGAGE == 'MORTGAGE':
        MORTGAGE = 1
    else:
        MORTGAGE = 0    
    # convert earliest_cr_line to year 
    earliest_cr_line = pd.to_datetime(earliest_cr_line, format='%Y-%m').year
    # convert data to Array
    input_data = np.array([
        loan_amnt,
        annual_inc,
        dti,
        bc_open_to_buy,
        revol_bal,
        fico,
        mo_sin_old_rev_tl_op,
        total_acc,
        acc_open_past_24mths,
        tot_cur_bal,
        earliest_cr_line,
        num_actv_bc_tl,
        mths_since_recent_bc,
        revol_util,
        num_tl_op_past_12m,
        delinq_2yrs,
        mort_acc,
        mths_since_recent_inq,
        term_36,
        application_type_Individual,
        inq_last_6mths,
        verification_status_Verified,
        num_rev_accts,
        verification_status_Source_Verified,
        pct_tl_nvr_dlq,
        mo_sin_rcnt_tl,
        purpose_small_business,
        NY, 
        purpose_credit_card, 
        MORTGAGE
    ]).reshape(1, -1)  # what is reshape(1, -1) for? -> 2 dimensional array with 1 row and 30 columns 

    # scale data
    input_data_scaled = scaler.transform(input_data)
    # make prediction
    y_pred_proba = model.predict_proba(input_data_scaled)[:, 1]
    # predict based on threshold
    y_filtered = (y_pred_proba >= threshold).astype(int)
    # check if y_filtered is 1 or 0
    if y_filtered[0] == 1:
        result = "Khách hàng có khả năng vỡ nợ"
    else:
        result = "Khách hàng không có khả năng vỡ nợ"
    # return result
    return jsonify({
    'success': True,
    'message': 'Dự đoán thành công',
    'result': result,
    'prediction': int(y_filtered[0]),
    'probability': float(y_pred_proba[0])
})

@app.route('/result')
def result_page():
    return render_template('result.html')

@app.route('/kiemtrano2')
def kiemtrano2_page():
    return render_template('model/model2/page_model2.html')    

@app.route('/api/kiem_tra_no2', methods=['POST'])
def kiemtrano2():
    data = request.get_json()
    # Extract features from the request data
    """
    'loan_amnt', 'acc_open_past_24mths', 'dti', 'fico_range_low',
       'annual_inc', 'emp_length', 'num_tl_op_past_12m', 'num_actv_rev_tl',
       'mo_sin_old_rev_tl_op', 'delinq_2yrs', 'inq_last_6mths',
       'mths_since_recent_inq', 'mort_acc', 'total_bc_limit', 'num_actv_bc_tl',
       'total_rev_hi_lim', 'revol_bal', 'mths_since_recent_bc', 'num_il_tl',
       'purpose_credit_card', 'percent_bc_gt_75',
       'verification_status_Verified', 'total_acc', 'home_ownership_RENT',
       'bc_util', 'bc_open_to_buy', 'purpose_small_business',
       'home_ownership_MORTGAGE', 'purpose_debt_consolidation',
       'verification_status_Source Verified'
    """
    loan_amnt = data['loan_amnt']
    acc_open_past_24mths = data['acc_open_past_24mths']
    dti = data['dti']
    fico_range_low = data['fico_range_low']
    annual_inc = data['annual_inc']
    emp_length = data['emp_length']
    num_tl_op_past_12m = data['num_tl_op_past_12m']
    num_actv_rev_tl = data['num_actv_rev_tl']
    mo_sin_old_rev_tl_op = data['mo_sin_old_rev_tl_op']
    delinq_2yrs = data['delinq_2yrs']
    inq_last_6mths = data['inq_last_6mths']
    mths_since_recent_inq = data['mths_since_recent_inq']
    mort_acc = data['mort_acc']
    total_bc_limit = data['total_bc_limit']
    num_actv_bc_tl = data['num_actv_bc_tl']
    total_rev_hi_lim = data['total_rev_hi_lim']
    revol_bal = data['revol_bal']
    mths_since_recent_bc = data['mths_since_recent_bc']
    num_il_tl = data['num_il_tl']
    purpose_credit_card = data['purpose']
    percent_bc_gt_75 = data['percent_bc_gt_75']
    verification_status_Verified = data['verification_status']
    total_acc = data['total_acc']
    home_ownership_RENT = data['home_ownership']
    bc_util = data['bc_util']
    bc_open_to_buy = data['bc_open_to_buy']
    purpose_small_business = data['purpose']
    home_ownership_MORTGAGE = data['home_ownership']
    purpose_debt_consolidation = data['purpose']
    verification_status_Source_Verified = data['verification_status']
    # Convert categorical variables to numerical values
    if purpose_credit_card == 'credit_card':
        purpose_credit_card = 1
    else:
        purpose_credit_card = 0
    
    if purpose_small_business == 'small_business':
        purpose_small_business = 1
    else:
        purpose_small_business = 0

    if purpose_debt_consolidation == 'debt_consolidation':
        purpose_debt_consolidation = 1
    else:
        purpose_debt_consolidation = 0

    if verification_status_Verified == 'Verified':
        verification_status_Verified = 1
    else:
        verification_status_Verified = 0

    if verification_status_Source_Verified == 'Source Verified':
        verification_status_Source_Verified = 1
    else:
        verification_status_Source_Verified = 0 
    
    if home_ownership_RENT == 'RENT':
        home_ownership_RENT = 1
    else:
        home_ownership_RENT = 0
    
    if home_ownership_MORTGAGE == 'MORTGAGE':
        home_ownership_MORTGAGE = 1
    else:
        home_ownership_MORTGAGE = 0

    # convert into array
    input_data = np.array([
    loan_amnt,
    acc_open_past_24mths,
    dti,
    fico_range_low,
    annual_inc,
    emp_length,
    num_tl_op_past_12m,
    num_actv_rev_tl,
    mo_sin_old_rev_tl_op,
    delinq_2yrs,
    inq_last_6mths,
    mths_since_recent_inq,
    mort_acc,
    total_bc_limit,
    num_actv_bc_tl,
    total_rev_hi_lim,
    revol_bal,
    mths_since_recent_bc,
    num_il_tl,
    purpose_credit_card,
    percent_bc_gt_75,
    verification_status_Verified,
    total_acc,
    home_ownership_RENT,
    bc_util,
    bc_open_to_buy,
    purpose_small_business,
    home_ownership_MORTGAGE,
    purpose_debt_consolidation,
    verification_status_Source_Verified
    ], dtype=float).reshape(1, -1) # 2 dimensional array with 1 row and 30 columns

    # predict with model2
    y_pred_proba2 = model2.predict_proba(input_data)[:, 1]
    # predict based on threshold2
    y_filtered2 = (y_pred_proba2 >= 0.34).astype(int)
    # check if y_filtered2 is 1 or 0
    if y_filtered2[0] == 1:
        result2 = "Khách hàng có khả năng vỡ nợ"
    else:
        result2 = "Khách hàng không có khả năng vỡ nợ"
    # return result2
    return jsonify({
        'success': True,
        'message': 'Dự đoán thành công',
        'result': result2,
        'prediction': int(y_filtered2[0]),
        'probability': float(y_pred_proba2[0])
    })



if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)  # debug=False cho production