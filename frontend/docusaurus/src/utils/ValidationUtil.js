// API request/response validation based on contract specifications
class ValidationUtil {
  // Define API contract schemas
  static get schemas() {
    return {
      chatRequest: {
        required: ['message'],
        fields: {
          message: {
            type: 'string',
            minLength: 1,
            maxLength: 10000
          },
          selected_text: {
            type: 'string',
            maxLength: 5000,
            required: false
          },
          session_id: {
            type: 'string',
            minLength: 1,
            required: false
          }
        }
      },
      chatResponse: {
        required: ['response', 'session_id'],
        fields: {
          response: {
            type: 'string',
            minLength: 1
          },
          session_id: {
            type: 'string',
            minLength: 1
          },
          sources: {
            type: 'array',
            maxItems: 100,
            required: false,
            itemValidator: (item) => this.validateString(item, 'sources[]', { minLength: 1, maxLength: 500 })
          },
          mode: {
            type: 'string',
            required: false
          },
          retrieved_chunks_count: {
            type: 'number',
            required: false
          },
          response_time: {
            type: 'number',
            required: false
          }
        }
      },
      healthResponse: {
        required: ['status', 'timestamp', 'dependencies'],
        fields: {
          status: {
            type: 'string',
            pattern: '^(healthy|unhealthy)$'
          },
          timestamp: {
            type: 'string',
            minLength: 1
          },
          dependencies: {
            type: 'object',
            required: false
          }
        }
      },
      ingestionResponse: {
        required: ['status'],
        fields: {
          status: {
            type: 'string',
            minLength: 1
          },
          pages_processed: {
            type: 'number',
            required: false
          },
          chunks_created: {
            type: 'number',
            required: false
          },
          message: {
            type: 'string',
            required: false
          }
        }
      }
    };
  }

  // Validate chat request payload against contract
  static validateChatRequest(payload) {
    return this.validatePayload(payload, this.schemas.chatRequest);
  }

  // Validate chat response from backend against contract
  static validateChatResponse(response) {
    return this.validatePayload(response, this.schemas.chatResponse);
  }

  // Validate health check response against contract
  static validateHealthResponse(response) {
    return this.validatePayload(response, this.schemas.healthResponse);
  }

  // Validate ingestion response against contract
  static validateIngestionResponse(response) {
    return this.validatePayload(response, this.schemas.ingestionResponse);
  }

  // Validate any request/response against a specific schema
  static validateAgainstSchema(payload, schemaName) {
    const schema = this.schemas[schemaName];
    if (!schema) {
      throw new Error(`Unknown schema: ${schemaName}`);
    }
    return this.validatePayload(payload, schema);
  }

  // Generic validation for any request payload
  static validatePayload(payload, schema) {
    const errors = [];

    if (typeof payload !== 'object' || payload === null) {
      errors.push({
        field: 'payload',
        message: 'Payload must be an object'
      });
      return {
        isValid: errors.length === 0,
        errors
      };
    }

    // Check required fields
    if (schema.required) {
      for (const field of schema.required) {
        if (payload[field] === undefined || payload[field] === null ||
            (typeof payload[field] === 'string' && payload[field].trim().length === 0)) {
          errors.push({
            field,
            message: `${field} is required`
          });
        }
      }
    }

    // Check field types and constraints
    if (schema.fields) {
      for (const [field, fieldSpec] of Object.entries(schema.fields)) {
        const value = payload[field];

        // Skip validation if field is not required and not provided
        if (value === undefined || value === null) {
          if (fieldSpec.required === true) {
            errors.push({
              field,
              message: `${field} is required`
            });
          }
          continue;
        }

        // Check type
        if (fieldSpec.type) {
          let isValidType = false;

          switch (fieldSpec.type) {
            case 'string':
              isValidType = typeof value === 'string';
              break;
            case 'number':
              isValidType = typeof value === 'number' && !isNaN(value);
              break;
            case 'boolean':
              isValidType = typeof value === 'boolean';
              break;
            case 'object':
              isValidType = typeof value === 'object' && value !== null && !Array.isArray(value);
              break;
            case 'array':
              isValidType = Array.isArray(value);
              break;
            default:
              isValidType = typeof value === fieldSpec.type;
          }

          if (!isValidType) {
            errors.push({
              field,
              message: `${field} must be of type ${fieldSpec.type}`
            });
            continue; // Skip further validation for this field if type is wrong
          }
        }

        // Check string constraints
        if (typeof value === 'string') {
          if (fieldSpec.minLength && value.length < fieldSpec.minLength) {
            errors.push({
              field,
              message: `${field} must be at least ${fieldSpec.minLength} characters`
            });
          }

          if (fieldSpec.maxLength && value.length > fieldSpec.maxLength) {
            errors.push({
              field,
              message: `${field} must not exceed ${fieldSpec.maxLength} characters`
            });
          }

          if (fieldSpec.pattern && !new RegExp(fieldSpec.pattern).test(value)) {
            errors.push({
              field,
              message: `${field} does not match required pattern`
            });
          }
        }

        // Check number constraints
        if (typeof value === 'number') {
          if (fieldSpec.min !== undefined && value < fieldSpec.min) {
            errors.push({
              field,
              message: `${field} must be at least ${fieldSpec.min}`
            });
          }

          if (fieldSpec.max !== undefined && value > fieldSpec.max) {
            errors.push({
              field,
              message: `${field} must not exceed ${fieldSpec.max}`
            });
          }
        }

        // Check array constraints
        if (Array.isArray(value)) {
          if (fieldSpec.minItems !== undefined && value.length < fieldSpec.minItems) {
            errors.push({
              field,
              message: `${field} must have at least ${fieldSpec.minItems} items`
            });
          }

          if (fieldSpec.maxItems !== undefined && value.length > fieldSpec.maxItems) {
            errors.push({
              field,
              message: `${field} must not have more than ${fieldSpec.maxItems} items`
            });
          }

          if (fieldSpec.itemValidator) {
            for (let i = 0; i < value.length; i++) {
              const itemValidation = fieldSpec.itemValidator(value[i], `${field}[${i}]`);
              if (!itemValidation.isValid) {
                errors.push(...itemValidation.errors);
              }
            }
          }
        }

        // Check nested object properties
        if (typeof value === 'object' && value !== null && !Array.isArray(value) && fieldSpec.properties) {
          for (const [propName, propSpec] of Object.entries(fieldSpec.properties)) {
            const propValue = value[propName];

            if (propValue === undefined || propValue === null) {
              if (propSpec.required) {
                errors.push({
                  field: `${field}.${propName}`,
                  message: `${field}.${propName} is required`
                });
              }
              continue;
            }

            // Validate nested property using recursive approach for basic types
            if (propSpec.type) {
              let isValidType = false;

              switch (propSpec.type) {
                case 'string':
                  isValidType = typeof propValue === 'string';
                  break;
                case 'number':
                  isValidType = typeof propValue === 'number' && !isNaN(propValue);
                  break;
                case 'boolean':
                  isValidType = typeof propValue === 'boolean';
                  break;
                default:
                  isValidType = typeof propValue === propSpec.type;
              }

              if (!isValidType) {
                errors.push({
                  field: `${field}.${propName}`,
                  message: `${field}.${propName} must be of type ${propSpec.type}`
                });
              }
            }
          }
        }
      }
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }

  // Validate a string field
  static validateString(value, fieldName, options = {}) {
    const errors = [];

    if (value === undefined || value === null) {
      if (options.required !== false) { // Default to required if not explicitly set to false
        errors.push({
          field: fieldName,
          message: `${fieldName} is required`
        });
      }
      return {
        isValid: errors.length === 0,
        errors
      };
    }

    if (typeof value !== 'string') {
      errors.push({
        field: fieldName,
        message: `${fieldName} must be a string`
      });
      return {
        isValid: errors.length === 0,
        errors
      };
    }

    if (options.minLength && value.length < options.minLength) {
      errors.push({
        field: fieldName,
        message: `${fieldName} must be at least ${options.minLength} characters`
      });
    }

    if (options.maxLength && value.length > options.maxLength) {
      errors.push({
        field: fieldName,
        message: `${fieldName} must not exceed ${options.maxLength} characters`
      });
    }

    if (options.pattern && !new RegExp(options.pattern).test(value)) {
      errors.push({
        field: fieldName,
        message: `${fieldName} does not match required pattern`
      });
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }

  // Validate an array field
  static validateArray(value, fieldName, options = {}) {
    const errors = [];

    if (value === undefined || value === null) {
      if (options.required !== false) {
        errors.push({
          field: fieldName,
          message: `${fieldName} is required`
        });
      }
      return {
        isValid: errors.length === 0,
        errors
      };
    }

    if (!Array.isArray(value)) {
      errors.push({
        field: fieldName,
        message: `${fieldName} must be an array`
      });
      return {
        isValid: errors.length === 0,
        errors
      };
    }

    if (options.minItems && value.length < options.minItems) {
      errors.push({
        field: fieldName,
        message: `${fieldName} must have at least ${options.minItems} items`
      });
    }

    if (options.maxItems && value.length > options.maxItems) {
      errors.push({
        field: fieldName,
        message: `${fieldName} must not have more than ${options.maxItems} items`
      });
    }

    if (options.itemValidator) {
      for (let i = 0; i < value.length; i++) {
        const itemValidation = options.itemValidator(value[i], `${fieldName}[${i}]`);
        if (!itemValidation.isValid) {
          errors.push(...itemValidation.errors);
        }
      }
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }

  // Validate an object field
  static validateObject(value, fieldName, options = {}) {
    const errors = [];

    if (value === undefined || value === null) {
      if (options.required !== false) {
        errors.push({
          field: fieldName,
          message: `${fieldName} is required`
        });
      }
      return {
        isValid: errors.length === 0,
        errors
      };
    }

    if (typeof value !== 'object' || Array.isArray(value)) {
      errors.push({
        field: fieldName,
        message: `${fieldName} must be an object`
      });
      return {
        isValid: errors.length === 0,
        errors
      };
    }

    if (options.properties) {
      for (const [propName, propSpec] of Object.entries(options.properties)) {
        const propValue = value[propName];
        let validator;

        switch (propSpec.type) {
          case 'string':
            validator = () => this.validateString(propValue, `${fieldName}.${propName}`, propSpec);
            break;
          case 'array':
            validator = () => this.validateArray(propValue, `${fieldName}.${propName}`, propSpec);
            break;
          case 'object':
            validator = () => this.validateObject(propValue, `${fieldName}.${propName}`, propSpec);
            break;
          default:
            // For other types, just check if required
            if (propSpec.required && (propValue === undefined || propValue === null)) {
              errors.push({
                field: `${fieldName}.${propName}`,
                message: `${fieldName}.${propName} is required`
              });
            }
            continue;
        }

        const validation = validator();
        if (!validation.isValid) {
          errors.push(...validation.errors);
        }
      }
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }

  // Validate API contract compliance for a specific endpoint
  static validateApiContract(endpoint, payload, method = 'request') {
    const validationMap = {
      '/api/v1/chat': {
        request: 'chatRequest',
        response: 'chatResponse'
      },
      '/health': {
        request: null, // GET request, no payload
        response: 'healthResponse'
      },
      '/api/v1/ingestion': {
        request: null, // Would be validated separately
        response: 'ingestionResponse'
      }
    };

    const endpointConfig = validationMap[endpoint];
    if (!endpointConfig) {
      return {
        isValid: false,
        errors: [{ field: 'endpoint', message: `Unknown endpoint: ${endpoint}` }]
      };
    }

    const schemaName = endpointConfig[method];
    if (!schemaName) {
      return {
        isValid: true,
        errors: []
      };
    }

    return this.validateAgainstSchema(payload, schemaName);
  }
}

export default ValidationUtil;