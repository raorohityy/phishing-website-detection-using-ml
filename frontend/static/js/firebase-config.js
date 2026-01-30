import { initializeApp } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-analytics.js";

const firebaseConfig = {
  apiKey: "AIzaSyDuhUXtueevtDgwP4RsfulrV2ko1x8M4Xg",
  authDomain: "phishing-website-detection-sys.firebaseapp.com",
  projectId: "phishing-website-detection-sys",
  storageBucket: "phishing-website-detection-sys.firebasestorage.app",
  messagingSenderId: "901980556504",
  appId: "1:901980556504:web:a5effb88caff7d21de9bad",
  measurementId: "G-KZMWR3GQQ9"
};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

export { app };
