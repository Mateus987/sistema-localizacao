const { GraphQLScalarType, Kind } = require('graphql');

const DateScalar = new GraphQLScalarType({
  name: 'Date',
  description: 'Custom scalar type for date',
  serialize(value) {
    // Assuming value is a JavaScript Date object
    return value.toISOString();
  },
  parseValue(value) {
    // Assuming value is a valid date string
    return new Date(value);
  },
  parseLiteral(ast) {
    if (ast.kind === Kind.STRING) {
      // Assuming ast.value is a valid date string
      return new Date(ast.value);
    }
    return null;
  },
});

module.exports = {
  DateScalar,
};
