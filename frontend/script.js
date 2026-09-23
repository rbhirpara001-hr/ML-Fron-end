// =====================================================
// BACKEND API URL
// =====================================================

const API_BASE_URL = "https://cardiorisk-backend.onrender.com";

console.log("Connected API Base URL:", API_BASE_URL);


// =====================================================
// DOM CONTENT LOADED
// =====================================================

document.addEventListener("DOMContentLoaded", () => {

    // =====================================================
    // ELEMENTS
    // =====================================================

    const form = document.getElementById("predictionForm");

    const heightInput = document.getElementById("height");
    const weightInput = document.getElementById("weight");

    const liveBmi = document.getElementById("liveBmi");
    const liveBmiBadge = document.getElementById("liveBmiBadge");

    const emptyState = document.getElementById("emptyState");
    const loadingState = document.getElementById("loadingState");
    const resultContent = document.getElementById("resultContent");

    const riskLabel = document.getElementById("riskLabel");
    const riskPercent = document.getElementById("riskPercent");
    const gaugeRing = document.getElementById("gaugeRing");

    const riskBadgeBox = document.getElementById("riskBadgeBox");
    const riskBadgeText = document.getElementById("riskBadgeText");

    const resBmi = document.getElementById("resBmi");
    const resBmiCat = document.getElementById("resBmiCat");

    const resBp = document.getElementById("resBp");
    const resBpCat = document.getElementById("resBpCat");

    const recommendationsList =
        document.getElementById("recommendationsList");

    const serverStatus =
        document.getElementById("serverStatus");


    // =====================================================
    // BACKEND HEALTH CHECK
    // =====================================================

    checkBackendHealth();

    async function checkBackendHealth() {

        try {

            const response = await fetch(
                `${API_BASE_URL}/api/health`
            );

            if (!response.ok) {

                throw new Error(
                    "Backend health check failed"
                );

            }

            const data = await response.json();

            console.log(
                "Backend Health:",
                data
            );


            if (
                data.status === "healthy" &&
                data.model_loaded === true &&
                data.scaler_loaded === true
            ) {

                if (serverStatus) {

                    serverStatus.innerHTML =
                        '<span class="status-dot online"></span>' +
                        '<span class="status-text">' +
                        'Backend API Connected' +
                        '</span>';

                }

            } else {

                throw new Error(
                    "Model or scaler is not loaded"
                );

            }

        } catch (error) {

            console.error(
                "Backend connection error:",
                error
            );


            if (serverStatus) {

                serverStatus.innerHTML =
                    '<span class="status-dot" ' +
                    'style="background:#f43f5e"></span>' +
                    '<span class="status-text" ' +
                    'style="color:#f43f5e">' +
                    'Backend Offline' +
                    '</span>';

            }

        }

    }


    // =====================================================
    // LIVE BMI
    // =====================================================

    function updateLiveBmi() {

        const height =
            parseFloat(
                heightInput.value
            ) || 0;

        const weight =
            parseFloat(
                weightInput.value
            ) || 0;


        if (
            height > 0 &&
            weight > 0
        ) {

            const bmi =
                weight /
                ((height / 100) ** 2);

            const roundedBmi =
                bmi.toFixed(1);


            liveBmi.textContent =
                `${roundedBmi} kg/m²`;


            if (bmi < 18.5) {

                liveBmiBadge.textContent =
                    "Underweight";

                liveBmiBadge.className =
                    "bmi-badge warning";

            }

            else if (bmi < 25) {

                liveBmiBadge.textContent =
                    "Normal";

                liveBmiBadge.className =
                    "bmi-badge normal";

            }

            else if (bmi < 30) {

                liveBmiBadge.textContent =
                    "Overweight";

                liveBmiBadge.className =
                    "bmi-badge warning";

            }

            else {

                liveBmiBadge.textContent =
                    "Obese";

                liveBmiBadge.className =
                    "bmi-badge warning";

            }

        }

        else {

            liveBmi.textContent =
                "-- kg/m²";

            liveBmiBadge.textContent =
                "--";

            liveBmiBadge.className =
                "bmi-badge warning";

        }

    }


    if (
        heightInput &&
        weightInput
    ) {

        heightInput.addEventListener(
            "input",
            updateLiveBmi
        );

        weightInput.addEventListener(
            "input",
            updateLiveBmi
        );

        updateLiveBmi();

    }


    // =====================================================
    // FORM SUBMIT
    // =====================================================

    if (form) {

        form.addEventListener(
            "submit",
            async (e) => {

                e.preventDefault();


                console.log(
                    "Prediction button clicked"
                );


                // =================================================
                // GET FORM DATA
                // =================================================

                const payload = {

                    age:
                        parseInt(
                            document.getElementById(
                                "age"
                            ).value
                        ),

                    gender:
                        parseInt(
                            document.getElementById(
                                "gender"
                            ).value
                        ),

                    height:
                        parseFloat(
                            document.getElementById(
                                "height"
                            ).value
                        ),

                    weight:
                        parseFloat(
                            document.getElementById(
                                "weight"
                            ).value
                        ),

                    ap_hi:
                        parseInt(
                            document.getElementById(
                                "ap_hi"
                            ).value
                        ),

                    ap_lo:
                        parseInt(
                            document.getElementById(
                                "ap_lo"
                            ).value
                        ),

                    cholesterol:
                        parseInt(
                            document.getElementById(
                                "cholesterol"
                            ).value
                        ),

                    gluc:
                        parseInt(
                            document.getElementById(
                                "gluc"
                            ).value
                        ),

                    smoke:
                        document.getElementById(
                            "smoke"
                        ).checked
                            ? 1
                            : 0,

                    alco:
                        document.getElementById(
                            "alco"
                        ).checked
                            ? 1
                            : 0,

                    active:
                        document.getElementById(
                            "active"
                        ).checked
                            ? 1
                            : 0

                };


                console.log(
                    "Sending payload:",
                    payload
                );


                // =================================================
                // LOADING UI
                // =================================================

                emptyState.classList.add(
                    "hidden"
                );

                resultContent.classList.add(
                    "hidden"
                );

                loadingState.classList.remove(
                    "hidden"
                );


                try {

                    // =============================================
                    // SEND REQUEST TO RENDER BACKEND
                    // =============================================

                    const response =
                        await fetch(
                            `${API_BASE_URL}/api/predict`,
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body:
                                    JSON.stringify(
                                        payload
                                    )
                            }
                        );


                    console.log(
                        "HTTP Status:",
                        response.status
                    );


                    // =============================================
                    // RESPONSE
                    // =============================================

                    const data =
                        await response.json();


                    console.log(
                        "Prediction Response:",
                        data
                    );


                    if (!response.ok) {

                        throw new Error(
                            data.error ||
                            `Server error: ${response.status}`
                        );

                    }


                    if (!data.success) {

                        throw new Error(
                            data.error ||
                            "Prediction failed"
                        );

                    }


                    // =============================================
                    // SHOW RESULT
                    // =============================================

                    renderResults(data);

                }

                catch (error) {

                    console.error(
                        "Prediction error:",
                        error
                    );


                    loadingState.classList.add(
                        "hidden"
                    );

                    emptyState.classList.remove(
                        "hidden"
                    );


                    alert(
                        "Prediction failed!\n\n" +
                        error.message
                    );

                }

            }
        );

    }


    // =====================================================
    // RENDER RESULTS
    // =====================================================

    function renderResults(data) {

        loadingState.classList.add(
            "hidden"
        );

        resultContent.classList.remove(
            "hidden"
        );


        // =================================================
        // RISK
        // =================================================

        const probability =
            Number(
                data.risk_probability
            );


        const isHigh =
            data.prediction === 1;


        riskLabel.textContent =
            data.risk_label;


        riskPercent.textContent =
            `${probability}%`;


        // =================================================
        // GAUGE
        // =================================================

        const angle =
            (probability / 100) * 360;


        const color =
            isHigh
                ? "#f43f5e"
                : "#10b981";


        gaugeRing.style.background =
            `conic-gradient(
                ${color} 0deg ${angle}deg,
                rgba(255,255,255,0.05)
                ${angle}deg
            )`;


        gaugeRing.style.boxShadow =
            isHigh
                ? "0 0 30px rgba(244,63,94,0.3)"
                : "0 0 30px rgba(16,185,129,0.3)";


        // =================================================
        // RISK BADGE
        // =================================================

        if (isHigh) {

            riskBadgeBox.className =
                "risk-badge-box high-risk";

            riskBadgeText.textContent =
                "High Cardiovascular Disease Risk";

        }

        else {

            riskBadgeBox.className =
                "risk-badge-box low-risk";

            riskBadgeText.textContent =
                "Low Cardiovascular Disease Risk";

        }


        // =================================================
        // HEALTH METRICS
        // =================================================

        if (data.health_metrics) {

            resBmi.textContent =
                `${data.health_metrics.bmi} kg/m²`;


            resBmiCat.textContent =
                data.health_metrics.bmi_category;


            resBp.textContent =
                `${data.health_metrics.systolic_bp} / ` +
                `${data.health_metrics.diastolic_bp}`;


            resBpCat.textContent =
                data.health_metrics.bp_category;

        }


        // =================================================
        // RECOMMENDATIONS
        // =================================================

        recommendationsList.innerHTML = "";


        if (
            data.recommendations &&
            data.recommendations.length > 0
        ) {

            data.recommendations.forEach(
                (recommendation) => {

                    const li =
                        document.createElement(
                            "li"
                        );


                    li.textContent =
                        recommendation;


                    recommendationsList.appendChild(
                        li
                    );

                }
            );

        }

    }

});