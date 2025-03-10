$(document).ready(function () {
    $(".department").each(function () {
        let departmentId = $(this).data("id");
        let subList = $("#subdepartments-" + departmentId);

        if (subList.length > 0) {
            let arrow = $("<span>").addClass("arrow").html("▶ ").css({
                "cursor": "pointer",
                "margin-right": "5px",
                "font-size": "14px"
            });

            $(this).prepend(arrow);
        }
    });

    $(".department").click(function (event) {
        event.preventDefault();
        let departmentId = $(this).data("id");
        let subList = $("#subdepartments-" + departmentId);
        let arrow = $(this).find(".arrow");

        if (subList.is(":visible")) {
            subList.hide();
            arrow.html("▶ ");
        } else {
            subList.show();
            arrow.html("▼ ");
        }
    });

    $(".select-department").click(function () {
        let departmentId = $(this).data("id");
        let positionsList = $("#positions-list");
        let existingPositions = $(`ul[data-department='${departmentId}']`);

        if (existingPositions.length) {
            existingPositions.remove();
            $(this).css("background-color", "#28a745").text("Выбрать");
        } else {
            $.getJSON(`/get_positions/${departmentId}/`, function (data) {
                if (data.positions.length === 0) {
                    alert("Нет доступных должностей для этого департамента.");
                    return;
                }

                let ul = $("<ul>").attr("data-department", departmentId);
                data.positions.forEach(function (position) {
                    let positionId = position.id;
                    let positionName = position.name;

                    if ($(`#positions-list li[data-id='${positionId}']`).length === 0) {
                        let listItem = $("<li>")
                            .addClass("position-item is-clickable")
                            .attr("data-id", positionId)
                            .css("display", "flex")
                            .css("align-items", "center");

                        let radio = $("<input>")
                            .attr("type", "radio")
                            .attr("name", "position")
                            .attr("value", positionId)
                            .css("margin-right", "8px");

                        listItem.append(radio).append(positionName);
                        ul.append(listItem);
                    }
                });

                positionsList.append(ul);
                $(this).css("background-color", "red").text("Убрать");
            }.bind(this));
        }
    });

    $(document).on("click", ".position-item", function () {
        let radio = $(this).find("input[type='radio']");
        if (!radio.prop("checked")) {
            radio.prop("checked", true).trigger("change");
        }
    });

    let mode = window.location.pathname.includes("/add_position/") ||
        window.location.pathname.includes("/edit_position/") ? "position_selection" : "default";

    let selectedDepartments = $("form").data("selected-departments") || [];


    function updateSelectionUI() {
        $(".select-department").each(function () {
            let departmentId = $(this).data("id");
            let container = $(this).parent();

            if (mode === "position_selection") {
                $(this).remove();
                if (container.find("input[type='checkbox']").length === 0) {
                    let checkbox = $("<input>")
                        .attr("type", "checkbox")
                        .attr("name", "departments")
                        .attr("value", departmentId)
                        .addClass("department-checkbox");


                    if (selectedDepartments.includes(departmentId)) {
                        checkbox.prop("checked", true);
                    }

                    container.append(checkbox);
                }
            } else {
                container.find("input[type='checkbox']").remove();
                if (container.find(".select-department").length === 0) {
                    let button = $("<button>")
                        .attr("type", "button")
                        .addClass("select-department select-btn")
                        .attr("data-id", departmentId)
                        .text("Выбрать");
                    container.append(button);
                }
            }
        });
    }

    updateSelectionUI();

    const checkboxes = $("input[type='checkbox'][name='departments']");
    const form = $("#position-form");

    checkboxes.on("change", function () {
        let checkedCount = checkboxes.filter(":checked").length;

        if (checkedCount > 3) {
            $(this).prop("checked", false);
            alert("Можно выбрать не более 3 департаментов!");
        }
    });


    form.on("submit", function (event) {
        let checkedCount = checkboxes.filter(":checked").length;

        if (checkedCount === 0) {
            alert("Выберите хотя бы 1 департамент!");
            event.preventDefault();
        }
    });
});