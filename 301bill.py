import streamlit as st
import pandas as pd

# definition of expenses and balances
if 'expenses' not in st.session_state:
    st.session_state.expenses = []
if 'balances' not in st.session_state:
    st.session_state.balances = pd.DataFrame(columns=["BQS", "JJ", "YXC", "RYF"], index=["BQS", "JJ", "YXC", "RYF"]).fillna(0)

st.title("301的账单")

#equation
def add_expense(description, amount, payer, share):
    if description and amount > 0 and payer and share:
        share_per_person = amount / (len(share) + 1)  # 计算每个人应付的金额
        st.session_state.expenses.append({
            "内容": description,
            "数额": amount,
            "谁付的": payer,
            "谁需要share": share,
            "每个人付多少": share_per_person
        })

        #balance
        for i in share:
            st.session_state.balances.loc[payer, i] -= share_per_person
            st.session_state.balances.loc[i, payer] += share_per_person

        st.success(f"账单 '{description}' 已添加")
    else:
        st.error("请完整填写所有信息")

# input
with st.form("expense_form", clear_on_submit = True):
    description = st.text_input("内容")
    amount = st.number_input("数额", min_value=0.0, step=0.01)
    payer = st.selectbox("谁付的", ["BQS", "JJ", "YXC", "RYF"])
    share = st.multiselect("谁需要share", ["BQS", "JJ", "YXC", "RYF"])
    submitted = st.form_submit_button("增加新条目")

    if description and amount > 0 and payer and share and submitted:
        add_expense(description, amount, payer, share)

# bill
if st.session_state.expenses:
    st.subheader("账单明细")
    for expense in st.session_state.expenses:
        st.write(f"{expense['内容']}: {expense['谁付的']} 付了 {expense['数额']} 元，分摊给 {', '.join(expense['谁需要share'])}，每人需要付 {expense['每个人付多少']:.2f} 刀")

# balance
if not st.session_state.balances.empty:
    st.subheader("余额")
    for person in st.session_state.balances.columns:
        for other_person in st.session_state.balances.index:
            balance = st.session_state.balances.loc[other_person, person]
            if balance > 0:
                st.write(f"{other_person} 需要给 {person} {balance:.2f} 刀")
