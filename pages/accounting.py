@app.route('/api/balance-sheet', methods=['GET'])
def get_balance_sheet():
    accounts = Account.query.all()
    return jsonify([account.to_dict() for account in accounts])

@app.route('/api/income-statement', methods=['GET'])
def get_income_statement():
    entries = JournalEntry.query.all()
    total_debit = sum(entry.debit for entry in entries)
    total_credit = sum(entry.credit for entry in entries)
    return jsonify({
        "total_debit": total_debit,
        "total_credit": total_credit,
        "net_income": total_credit - total_debit
    })

@app.route('/api/account/<account_name>', methods=['GET'])
def get_account_balance(account_name):
    account = Account.query.filter_by(name=account_name).first()
    if not account:
        return jsonify({"message": "Account not found"}), 404
    return jsonify(account.to_dict())
