const exPSA_brands = {{ exPSA_brands | tojson }};
const exFCA_brands = {{ exFCA_brands | tojson }};

function updateBrandOptions() {
    const exType = document.getElementById("exType").value;
    const brandSelect = document.getElementById("brand");
    brandSelect.innerHTML = "";

    const brands = exType === "exPSA" ? exPSA_brands : exFCA_brands;

    brands.forEach(brand => {
        const option = document.createElement("option");
        option.value = brand;
        option.text = brand;
        brandSelect.add(option);
    });
}

window.onload = function () {
    const today = new Date().toISOString().split("T")[0];
    document.getElementById("date").setAttribute("min", today);
    updateBrandOptions();
};
