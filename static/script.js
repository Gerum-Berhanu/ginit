const solveBtn = document.getElementById("solve-btn");
const solnCont = document.getElementById("solution-cont");

solveBtn.addEventListener("click", async (e)=>{
    const equation = document.getElementById("equation-input");
    const lowerBound = document.getElementById("lower-input");
    const upperBound = document.getElementById("upper-input");

    const formData = new FormData();
    formData.append("equation", equation.value);
    formData.append("lowerBound", lowerBound.value);
    formData.append("upperBound", upperBound.value);

    const response = await fetch("/solve", {
        method: "POST",
        body: formData
    });
    const data = await response.json();

    const result = (!data.message) ? data.solution : data.message;

    const lowerValue = lowerBound.value ? lowerBound.value : -100;
    const upperValue = upperBound.value ? upperBound.value : 100;

    let newElt = document.createElement("div");
    newElt.innerHTML = `
    <div class="w-full flex flex-col">
        <div class="bg-black/30 p-4 rounded-t-md border-2 border-black/10 break-words flex justify-between">
            <div class="w-2/3 font-bold text-xl">${equation.value}</div>
            <div class="w-1/3 flex gap-2 justify-evenly">
                <div class="text-white font-bold bg-sky-100/10 p-2 rounded-md">Lower ${lowerValue}</div>
                <div class="text-white font-bold bg-sky-100/10 p-2 rounded-md">Upper ${upperValue}</div>
            </div>
        </div>
        <div class="bg-white/50 p-4 rounded-b-md border-2 border-black/10 break-words">${JSON.stringify(result, null, 2)}</div>
    </div>
    `;
    solnCont.insertBefore(newElt, solnCont.firstChild);

    equation.value = "";
    lowerBound.value = "";
    upperBound.value = "";
});