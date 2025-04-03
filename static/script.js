const solveBtn = document.getElementById("solve-btn");
const solnCont = document.getElementById("solution-cont");

solveBtn.addEventListener("click", async (e)=>{
    const equation = document.getElementById("equation-input").value;
    const formData = new FormData();
    formData.append("equation", equation);

    const response = await fetch("/solve", {
        method: "POST",
        body: formData
    });
    const data = await response.json();

    const result = (!data.message) ? data.solution : data.message;

    let newElt = document.createElement("div");
    newElt.innerHTML = `
    <div class="w-full flex flex-col">
        <div class="bg-black/30 p-4 rounded-t-md border-2 border-black/10 break-words">${equation}</div>
        <div class="bg-white/50 p-4 rounded-b-md border-2 border-black/10 break-words">${JSON.stringify(result, null, 2)}</div>
    </div>
    `;
    solnCont.insertBefore(newElt, solnCont.firstChild);
});