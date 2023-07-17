function showGraph(timeline)
{
    const dateToday = new Date();

    let day = dateToday.getDate();
    let month = dateToday.getMonth() + 1;
    let year = dateToday.getFullYear();

    let currentDate = '${day}-${month}-${year}';
    console.log(currentDate);

    if(timeline=='ALLTIME')
    {
        plotGraph('31-03-2011',currentDate)
    }
    else if(timeline=='1Y')
    {
        year=dateToday.getFullYear() - 1;
        let lastYrDate='${day}-${month}-${year}';
        plotGraph(lastYrDate,currentDate)
    }
}

function custom()
{
    var date1;
    var date2;
    plotGraph(date1,date2);
}

function plotGraph(dateFrom,dateTo)
{
    let xValues = [50,60,70,80,90,100,110,120];
    let yValues = [7,8,8,9,9,9,10,11];
    new Chart("DashboardPerformanceChart", {type: "line",data: {labels: xValues,datasets: [{borderColor:"rgba(28, 80, 157, 1.0)",data: yValues}]}});
}
