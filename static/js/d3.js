fetch("/departments/tree/data")
    .then(response => response.json())
    .then(data => drawTree({ name: "Банк", children: data }));

function drawTree(treeData) {
    const width = 1200, height = 600;

    const svg = d3.select("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", `0 0 ${width} ${height}`)
        .attr("preserveAspectRatio", "xMidYMid meet")
        .style("overflow", "visible");

    const g = svg.append("g").attr("transform", "translate(50, 50)");

    const treeLayout = d3.tree().size([height - 100, width - 200]);
    const root = d3.hierarchy(treeData);
    treeLayout(root);

    g.selectAll(".link")
        .data(root.links())
        .enter().append("path")
        .attr("class", "link")
        .attr("fill", "none")
        .attr("stroke", "black")
        .attr("stroke-width", 1.5)
        .attr("d", d3.linkHorizontal()
            .x(d => d.y)
            .y(d => d.x)
        );

    const node = g.selectAll(".node")
        .data(root.descendants())
        .enter().append("g")
        .attr("class", "node")
        .attr("transform", d => `translate(${d.y},${d.x})`);

    node.each(function (d) {
        const maxWidth = 100;
        const words = d.data.name.split(" ");
        let lines = [];
        let currentLine = "";

        words.forEach(word => {
            if ((currentLine + " " + word).trim().length * 6 < maxWidth) {
                currentLine += (currentLine ? " " : "") + word;
            } else {
                lines.push(currentLine);
                currentLine = word;
            }
        });
        if (currentLine) lines.push(currentLine);

        const rectHeight = lines.length * 18 + 40;

        const group = d3.select(this);
        console.log(d.data);

        group.append("rect")
            .attr("id", `node-${d.data.pk}`)
            .attr("width", maxWidth + 20)
            .attr("height", rectHeight)
            .attr("x", -((maxWidth + 20) / 2))
            .attr("y", -(rectHeight / 2))
            .attr("fill", "lightgreen")
            .attr("stroke", "blue");

        const textGroup = group.append("text")
            .attr("text-anchor", "middle")
            .attr("fill", "black");

        lines.forEach((line, i) => {
            textGroup.append("tspan")
                .attr("x", 0)
                .attr("dy", i === 0 ? "0" : "1.2em")
                .text(line);
        });

        const buttonGroup = group.append("g")
            .attr("transform", `translate(0, ${rectHeight / 2 - 18})`);

        const buttons = [
            { id: `add-btn-${d.data.pk}`, action: 'add', label: "+", },
            { id: `edit-btn-${d.data.pk}`, action: 'edit', label: "✎", },
            { id: `delete-btn-${d.data.pk}`, action: 'delete', label: "🗑", }
        ];

        buttons.forEach((btn, i) => {
            if (d.depth === 0 && (btn.label === "✎" || btn.label === "🗑")) {
                return;
            }
            const xPos = (i - 1) * 30;

            const button = buttonGroup.append("a")
                .attr("id", btn.id)
                .attr("href", `/${btn.action}_department/${d.data.pk ?? 0}`)
                .attr("transform", `translate(${xPos}, 0)`)
                .style("cursor", "pointer")

            button.append("rect")
                .attr("width", 24)
                .attr("height", 24)
                .attr("x", -12)
                .attr("y", 0)
                .attr("fill", "white")
                .attr("stroke", "black")
                .attr("rx", 5);

            button.append("text")
                .attr("x", 0)
                .attr("y", 16)
                .attr("text-anchor", "middle")
                .attr("fill", "black")
                .attr("font-size", "14px")
                .text(btn.label);
        });
    });
}