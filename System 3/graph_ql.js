const express = require('express');
const { graphqlHTTP } = require('express-graphql');
const { buildSchema } = require('graphql');
const { DateScalar } = require("./graph_ql_date_scalar");

const sqlite3 = require('sqlite3').verbose();

// Connect to the SQLite database (or create a new one if it doesn't exist)
const db = new sqlite3.Database('database.sqlite3');

// Define GraphQL schema
const schema = buildSchema(`
  scalar Date

  type Dispositivo {
    id_dispositivo: String
    marca: String
    quantidade_pos: Int
    total_km: Float
    data: Date
  }

  type Query {
    geral: [Dispositivo]
    por_dispo(id_dispositivo: String): [Dispositivo]
    por_marca(marca: String): [Dispositivo]
  }
`);

// Define resolvers
const resolvers = {
    geral: () => {
        // Query data from the SQLite database
        return new Promise((resolve, reject) => {
            let query = `
        SELECT dispo.id_dispositivo, dispo.marca, dispo_info.quantidade_pos, dispo_info.total_km, dispo_info.data
        FROM dispositivo AS dispo
        LEFT JOIN dispo_info ON dispo.id_dispositivo = dispo_info.id_dispositivo
        ORDER BY data DESC
      `;

            db.all(query, (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows);
                }
            });
        });
    },

    por_dispo: (data) => {
        // Query data from the SQLite database
        return new Promise((resolve, reject) => {
            let query = `
        SELECT dispo.id_dispositivo, dispo.marca, dispo_info.quantidade_pos, dispo_info.total_km, dispo_info.data
        FROM dispositivo AS dispo
        LEFT JOIN dispo_info ON dispo.id_dispositivo = dispo_info.id_dispositivo
        WHERE dispo.id_dispositivo = ?
        ORDER BY data DESC
      `;

            db.all(query, [data.id_dispositivo], (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows);
                }
            });
        });
    },

    por_marca: (data) => {
        // Query data from the SQLite database
        return new Promise((resolve, reject) => {
            let query = `
        SELECT dispo.id_dispositivo, dispo.marca, dispo_info.quantidade_pos, dispo_info.total_km, dispo_info.data
        FROM dispositivo AS dispo
        LEFT JOIN dispo_info ON dispo.id_dispositivo = dispo_info.id_dispositivo
        WHERE dispo.marca = ?
        ORDER BY data DESC
      `;

            db.all(query, [data.marca], (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows);
                }
            });
        });
    },
};

// Create an express app
const app = express();

// Set up GraphQL middleware
app.use(
    '/graphql',
    graphqlHTTP({
        schema: schema,
        rootValue: resolvers,
        graphiql: true, // Enable GraphiQL interface for testing
    })
);

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}/graphql`);
});
