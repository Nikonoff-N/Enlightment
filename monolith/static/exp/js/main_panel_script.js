// #region open close trays

function switchStudents() {
    let elem = document.getElementById('main-studentrow')
    if (elem.classList.contains('main-full')){
        elem.classList.remove('main-full')
        elem.classList.add('main-short')
    }else{
        elem.classList.add('main-full')
        elem.classList.remove('main-short')
    }
}

function switchGroups() {
    let elem = document.getElementById('main-grouprow')
    if (elem.classList.contains('main-full')){
        elem.classList.remove('main-full')
        elem.classList.add('main-short')
    }else{
        elem.classList.add('main-full')
        elem.classList.remove('main-short')
    }
}

// #endregion

// #region open close dialogs

const detailsDialog = document.getElementById("dialog");

function openDetails(){
    detailsDialog.showModal();
}
function closeDetails(){
    detailsDialog.close();
}

// const favDialog = document.getElementById("favDialog");
// const confirmBtn = favDialog.querySelector("#confirmBtn");
// const cancelBtn = favDialog.querySelector("#cancelBtn");
// // "Show the dialog" button opens the <dialog> modally
// showButton.addEventListener("click", () => {
//     favDialog.showModal();
// });
// cancelBtn.addEventListener("click", () => {
//     favDialog.close();
// })
// confirmBtn.addEventListener("click", () => {
//     favDialog.close();
// })

// const GroupshowButton = document.getElementById("GroupshowDialog");
// const GroupfavDialog = document.getElementById("groupDialog");
// const GroupconfirmBtn = GroupfavDialog.querySelector("#groupconfirmBtn");
// const GroupcancelBtn = GroupfavDialog.querySelector("#groupcancelBtn");
// // "Show the dialog" button opens the <dialog> modally
// GroupshowButton.addEventListener("click", () => {
//     GroupfavDialog.showModal();
// });
// GroupcancelBtn.addEventListener("click", () => {
//     GroupfavDialog.close();
// })
// GroupconfirmBtn.addEventListener("click", () => {
//     GroupfavDialog.close();
// })
// #endregion

const StudentListElement = document.querySelector(`#student-list`);
const StudentElements = StudentListElement.querySelectorAll(`.draggableStudent`);
const groupListElement = document.querySelector(`#group-list`);
//const GroupElements = groupListElement.querySelectorAll(`.studcard`);
const StudIdInput = document.querySelector(`#studentId`);
const GroupIdInput = document.querySelector(`#groupId`);

// Перебираем все элементы списка и присваиваем нужное значение
for (const student of StudentElements) {
    student.draggable = true;
}
//refreshDrops()
function refreshDrops() {
    console.log('refresing!')
    let GroupElements = groupListElement.querySelectorAll(`.main-card`);
    for (const group of GroupElements) {//поменяй оф на ин и сведи себя с ума
        group.addEventListener("dragenter", (event) => {
            event.preventDefault();
            const activeElement = StudentListElement.querySelector(`.selected`);
            const currentElement = event.target;
            console.log(`Drag student ${activeElement.id} enter group ${currentElement.id}`)
        });
        group.addEventListener("dragover", (event) => {
            event.preventDefault();
        });
        group.addEventListener("drop", (event) => {
            const activeElement = StudentListElement.querySelector(`.selected`);
            console.log(`student ${activeElement.id} droped to group ${group.id}`)
            StudIdInput.value = activeElement.id
            GroupIdInput.value = group.id
            htmx.trigger("#group-list", "my-custom-event", {});
            event.preventDefault();
        });
    }
}


StudentListElement.addEventListener(`dragstart`, (evt) => {
    console.log("drag_started")
    evt.target.classList.add(`selected`);
    refreshDrops()
})

StudentListElement.addEventListener(`dragend`, (evt) => {
    evt.target.classList.remove(`selected`);
    console.log("drag_ended")
});


