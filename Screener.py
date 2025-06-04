from flask import Flask, render_template, jsonify
app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/scan')
def run_scan():
    analyzer = GrowthAnalyzer()
    data = TechStockData()

    results = []
    for ticker in data.tech_tickers[:50]:  # Limit for demo
        stock_data = data.get_historical_data(ticker)
        if stock_data:
            periods = analyzer.find_explosive_periods(stock_data['historical'])
            if periods:
                analysis = analyzer.analyze_pre_conditions(stock_data['historical'], periods[0])
                results.append({
                    'ticker': ticker,
                    'analysis': analysis,
                    'info': stock_data['info']
                })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
