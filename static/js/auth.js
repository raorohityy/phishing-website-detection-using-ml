import { getAuth, signInWithPopup, GoogleAuthProvider, createUserWithEmailAndPassword, signInWithEmailAndPassword, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-auth.js";
import { app } from "./firebase-config.js";

const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();

export function loginWithGoogle() {
    signInWithPopup(auth, googleProvider)
        .then((result) => {
            window.location.href = "/";
        })
        .catch((error) => {
            console.error(error);
            alert("Google Sign-In caught error: " + error.message);
        });
}

export function signupWithEmail(email, password) {
    createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            window.location.href = "/";
        })
        .catch((error) => {
            console.error(error);
            alert("Signup Error: " + error.message);
        });
}

export function loginWithEmail(email, password) {
    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            window.location.href = "/";
        })
        .catch((error) => {
            console.error(error);
            alert("Login Error: " + error.message);
        });
}

export function logout() {
    signOut(auth).then(() => {
        window.location.href = "/login";
    }).catch((error) => {
        console.error(error);
    });
}

export function monitorAuthState() {
    onAuthStateChanged(auth, (user) => {
        const loginLink = document.getElementById("nav-login");
        const signupLink = document.getElementById("nav-signup");
        const logoutLink = document.getElementById("nav-logout");

        if (user) {
            if (loginLink) loginLink.style.display = 'none';
            if (signupLink) signupLink.style.display = 'none';
            if (logoutLink) {
                logoutLink.style.display = 'block';
                logoutLink.onclick = logout;
            }
        } else {
            if (loginLink) loginLink.style.display = 'block';
            if (signupLink) signupLink.style.display = 'block';
            if (logoutLink) logoutLink.style.display = 'none';
        }
    });
}
