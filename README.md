# SafeNest AI 🏠
### Turning Raw Inspection Data into Actionable Safety Intelligence

**SafeNest AI** is a multimodal Generative AI platform designed to revolutionize property inspections. By combining computer vision, natural language processing, and advanced reasoning, it transforms messy photos and handwritten notes into instant, objective safety reports.

---

## 🚨 The Challenge
Traditional home inspections are slow, subjective, and often miss critical defects. Homebuyers frequently discover major issues only after moving in, while professional inspectors spend hours manually compiling data into reports.

## 💡 The Solution
SafeNest AI provides an intelligent assistant that handles the heavy lifting:
- **Instant Defect Detection**: Spot cracks, dampness, mold, and hazards directly from photos.
- **Risk Prioritization**: Automated scoring to tell you exactly how safe a property is.
- **Real-Time Cost Forecasting**: Estimates for repairs to help with financial planning.
- **Multi-Language Support**: Fully localized for English, Hindi, Tamil, Telugu, Kannada, and Malayalam.
- **Interactive AI Chatbot**: A dedicated assistant to answer follow-up questions about your specific inspection results.

---

## 🛠️ Getting Started

### Prerequisites
- **Python 3.8+**
- **API Keys**: You will need an OpenAI API key (and optionally a Grok API key for enhanced analysis).

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/lakshmanjasyal/codex.git
   cd codex/safeNest
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your credentials**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_key_here
   GROK_API_KEY=your_grok_key_here
   ```

5. **Launch SafeNest AI**
   ```bash
   streamlit run app.py
   ```

---

## 🤝 Contributing
We love community contributions! To help grow SafeNest AI:

1. **Fork** the repository.
2. Create a **Branch** (`git checkout -b feature/AmazingFeature`).
3. **Commit** your changes (`git commit -m 'Added some AmazingFeature'`).
4. **Push** to your fork (`git push origin feature/AmazingFeature`).
5. Open a **Pull Request**.

---

## 📸 Project Gallery

<p align="center">
  <img src="https://github.com/user-attachments/assets/aff4ed0d-ffd3-41ae-88d7-68a4e16d2d5f" width="45%" alt="Dashboard Overview" />
  <img src="https://github.com/user-attachments/assets/59259122-ac32-4685-a9b8-83a0ccb398ff" width="45%" alt="Defect Detection" />
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/075ee5e2-18d5-425b-8418-76e4f4c9e8fa" width="45%" alt="Risk Scoring" />
  <img src="https://github.com/user-attachments/assets/fc046320-2b39-4e5f-b909-68ad1d65592b" width="45%" alt="Chat Interface" />
</p>

---
*Built for the future of safe housing.*
