{% extends "product/base.html" %}
{% block title %}Dashboard{% endblock %}
{% block topbar %}Dashboard{% endblock %}
{% block content %}




<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Payments - Dark Theme</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: black;
            color: #e5e5e5;
            min-height: 100vh;
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }

        .header {
            text-align: center;
            margin-bottom: 3rem;
            position: relative;
        }

        .header::before {
            content: '';
            position: absolute;
            top: -20px;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 4px;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ef4444);
            border-radius: 2px;
        }

        h2 {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #ffffff 0%, #e5e5e5 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }

        .subtitle {
            color: #a1a1aa;
            font-size: 1.1rem;
            font-weight: 400;
        }

        .table-container {
            background: black;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            overflow: hidden;
            backdrop-filter: blur(20px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
        }

        .table-container:hover {
            transform: translateY(-2px);
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.1);
        }

        .table {
            width: 100%;
            border-collapse: collapse;
            background: transparent;
        }

        .table thead {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        }

        .table th {
            padding: 1.5rem 1.25rem;
            text-align: left;
            font-weight: 600;
            font-size: 0.9rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: #f1f5f9;
            border: none;
            position: relative;
        }

        .table th::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        }

        .table td {
            padding: 1.25rem;
            border: none;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
            font-size: 0.95rem;
        }

        .table tbody tr {
            transition: all 0.3s ease;
            position: relative;
        }

        .table tbody tr:hover {
            background: rgba(255, 255, 255, 0.03);
            transform: translateX(4px);
        }

        .table tbody tr:hover::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3px;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            border-radius: 0 2px 2px 0;
        }

        .item-name {
            font-weight: 600;
            color: #f8fafc;
        }

        .amount {
            font-weight: 700;
            font-size: 1.05rem;
            color: #10b981;
            font-family: 'SF Mono', 'Monaco', 'Inconsolata', monospace;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            padding: 0.5rem 1rem;
            border-radius: 50px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            position: relative;
            overflow: hidden;
        }

        .badge::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: left 0.6s;
        }

        .badge:hover::before {
            left: 100%;
        }

        .badge-success {
            background: linear-gradient(135deg, #059669 0%, #10b981 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        }

        .badge-warning {
            background: linear-gradient(135deg, #d97706 0%, #f59e0b 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
        }

        .badge-danger {
            background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
        }

        .date {
            color: #a1a1aa;
            font-size: 0.9rem;
            font-family: 'SF Mono', 'Monaco', 'Inconsolata', monospace;
        }

        .empty-state {
            text-align: center;
            padding: 4rem 2rem;
            color: #71717a;
        }

        .empty-state-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
            opacity: 0.3;
        }

        .empty-state-text {
            font-size: 1.1rem;
            font-weight: 500;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                padding: 1rem 0.5rem;
            }

            h2 {
                font-size: 2rem;
            }

            .table-container {
                border-radius: 12px;
                margin: 0 -0.5rem;
            }

            .table {
                font-size: 0.85rem;
            }

            .table th,
            .table td {
                padding: 1rem 0.75rem;
            }

            .table thead {
                display: none;
            }

            .table tbody tr {
                display: block;
                margin-bottom: 1rem;
                background: rgba(255, 255, 255, 0.02);
                border-radius: 12px;
                padding: 1rem;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }

            .table tbody td {
                display: flex;
                justify-content: space-between;
                align-items: center;
                border: none;
                padding: 0.5rem 0;
            }

            .table tbody td::before {
                content: attr(data-label);
                font-weight: 600;
                color: #a1a1aa;
                text-transform: uppercase;
                font-size: 0.75rem;
                letter-spacing: 0.05em;
                flex: 1;
            }

            .table tbody td:last-child {
                border-bottom: none;
            }
        }

        /* Scrollbar Styling */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.02);
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.2);
        }

        /* Loading Animation */
        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }

        .loading {
            position: relative;
            overflow: hidden;
        }

        .loading::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            animation: shimmer 2s infinite;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>My Payments</h2>
            <p class="subtitle">Track your payment history and status</p>
        </div>
        
        <div class="table-container">
            <table class="table">
                <thead>
                    <tr>
                        <th>Item</th>
                        <th>Amount</th>
                        <th>Status</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- Sample data for demonstration -->
                    <tr>
                        <td class="item-name" data-label="Item">Premium Subscription</td>
                        <td class="amount" data-label="Amount">$29.99</td>
                        <td data-label="Status">
                            <span class="badge badge-success">Completed</span>
                        </td>
                        <td class="date" data-label="Date">Jan 15, 2025 14:30</td>
                    </tr>
                    <tr>
                        <td class="item-name" data-label="Item">Cloud Storage</td>
                        <td class="amount" data-label="Amount">$9.99</td>
                        <td data-label="Status">
                            <span class="badge badge-warning">Pending</span>
                        </td>
                        <td class="date" data-label="Date">Jan 14, 2025 09:15</td>
                    </tr>
                    <tr>
                        <td class="item-name" data-label="Item">API Access</td>
                        <td class="amount" data-label="Amount">$99.00</td>
                        <td data-label="Status">
                            <span class="badge badge-danger">Failed</span>
                        </td>
                        <td class="date" data-label="Date">Jan 12, 2025 16:45</td>
                    </tr>
                    <tr>
                        <td class="item-name" data-label="Item">Domain Registration</td>
                        <td class="amount" data-label="Amount">$12.99</td>
                        <td data-label="Status">
                            <span class="badge badge-success">Completed</span>
                        </td>
                        <td class="date" data-label="Date">Jan 10, 2025 11:22</td>
                    </tr>
                    <!-- Uncomment below for empty state -->
                    <!--
                    <tr>
                        <td colspan="4" class="empty-state">
                            <div class="empty-state-icon">💳</div>
                            <div class="empty-state-text">No payments found.</div>
                        </td>
                    </tr>
                    -->
                </tbody>
            </table>
        </div>
    </div>

    <script>
        // Add subtle animations and interactions
        document.addEventListener('DOMContentLoaded', function() {
            const rows = document.querySelectorAll('.table tbody tr');
            
            rows.forEach((row, index) => {
                row.style.opacity = '0';
                row.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    row.style.transition = 'all 0.6s ease';
                    row.style.opacity = '1';
                    row.style.transform = 'translateY(0)';
                }, index * 100);
            });

            // Add click effects to badges
            const badges = document.querySelectorAll('.badge');
            badges.forEach(badge => {
                badge.addEventListener('click', function() {
                    this.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        this.style.transform = 'scale(1)';
                    }, 150);
                });
            });
        });
    </script>
</body>
{% endblock %}
