# Vanguard Holdings Download Instructions

Vanguard does not allow automated downloading of their holdings data. Please follow these steps to manually download the files for the Vanguard funds in your portfolio.

1.  **Create the directory** (if it doesn't exist):
    `data/holdings_files/`

2.  **Download the CSV files** for the following funds:

    *   **VOO (S&P 500 ETF)**:
        *   Go to: https://investor.vanguard.com/investment-products/etfs/profile/voo#portfolio-composition
        *   Click "Export to CSV" (usually near the holdings table).
        *   Save as: `data/holdings_files/VOO_holdings.csv`

    *   **VTI (Total Stock Market ETF)**:
        *   Go to: https://investor.vanguard.com/investment-products/etfs/profile/vti#portfolio-composition
        *   Save as: `data/holdings_files/VTI_holdings.csv`

    *   **VUG (Growth ETF)**:
        *   Go to: https://investor.vanguard.com/investment-products/etfs/profile/vug#portfolio-composition
        *   Save as: `data/holdings_files/VUG_holdings.csv`

    *   **VTV (Value ETF)**:
        *   Go to: https://investor.vanguard.com/investment-products/etfs/profile/vtv#portfolio-composition
        *   Save as: `data/holdings_files/VTV_holdings.csv`

    *   **VXUS (Total International Stock ETF)**:
        *   Go to: https://investor.vanguard.com/investment-products/etfs/profile/vxus#portfolio-composition
        *   Save as: `data/holdings_files/VXUS_holdings.csv`

    *   **VIG (Dividend Appreciation ETF)**:
        *   Go to: https://investor.vanguard.com/investment-products/etfs/profile/vig#portfolio-composition
        *   Save as: `data/holdings_files/VIG_holdings.csv`

    *   **VYM (High Dividend Yield ETF)**:
        *   Go to: https://investor.vanguard.com/investment-products/etfs/profile/vym#portfolio-composition
        *   Save as: `data/holdings_files/VYM_holdings.csv`

    *   **VNQ (Real Estate ETF)**:
        *   Go to: https://investor.vanguard.com/investment-products/etfs/profile/vnq#portfolio-composition
        *   Save as: `data/holdings_files/VNQ_holdings.csv`

    *   **VGT (Information Technology ETF)**:
        *   Go to: https://investor.vanguard.com/investment-products/etfs/profile/vgt#portfolio-composition
        *   Save as: `data/holdings_files/VGT_holdings.csv`

    *   **VWO (Emerging Markets Stock ETF)**:
        *   Go to: https://investor.vanguard.com/investment-products/etfs/profile/vwo#portfolio-composition
        *   Save as: `data/holdings_files/VWO_holdings.csv`

    *   **VEA (FTSE Developed Markets ETF)**:
        *   Go to: https://investor.vanguard.com/investment-products/etfs/profile/vea#portfolio-composition
        *   Save as: `data/holdings_files/VEA_holdings.csv`

3.  **Run the processing script** (once you have downloaded the files):
    ```bash
    python3 process_holdings.py
    ```
