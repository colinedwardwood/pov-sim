package com.example.springboot;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@RestController
@CrossOrigin(origins = "http://localhost:3000") // Allow requests from React app
public class AirlinesController {
	private static final Logger logger = LoggerFactory.getLogger(AirlinesController.class);
	private static String[] airlines = { "AA", "DL", "UA" };

	@Operation(summary = "Index", description = "No-op hello world")
	@GetMapping("/")
	public String index() {
		logger.info("Index endpoint called");
		return "Greetings from Spring Boot!";
	}

	@Operation(summary = "Health check", description = "Performs a simple health check")
	@GetMapping("/health")
	public String health() {
		logger.info("Health check endpoint called");
		return "Health check passed!";
	}

	@GetMapping("/airlines")
	@Operation(summary = "Get airlines", description = "Fetch a list of airlines")
	public String getUserById(
			@Parameter(description = "Optional flag - set raise to true to raise an exception") 
			@RequestParam(value = "raise", required = false, defaultValue = "false") boolean raise) {
		logger.info("Airlines endpoint called with raise={}", raise);
		if (raise) {
			logger.error("Exception intentionally raised in airlines endpoint");
			throw new RuntimeException("Exception raised");
		}
		logger.info("Returning {} airlines", airlines.length);
		return String.join(", ", airlines);
	}
}
