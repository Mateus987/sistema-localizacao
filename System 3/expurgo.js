const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('database.sqlite3');

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function expurgo() {
    while (true) {
        const currentDate = new Date();
        const fiveDaysAgo = new Date(currentDate.getTime() - 5 * 24 * 60 * 60 * 1000);
        const formattedFiveDaysAgo = fiveDaysAgo.toISOString().slice(0, 19).replace("T", " ");

        const deleteQuery = `DELETE FROM dispo_info WHERE data < ?`;

        db.run(deleteQuery, [formattedFiveDaysAgo], function (err) {
            if (err) {
                console.error(err.message);
            } else {
                console.log(`Records older than 5 days ago deleted successfully.`);
            }
        });

        await sleep(30000);
    }
}

expurgo();