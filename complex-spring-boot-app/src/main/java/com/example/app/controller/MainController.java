package com.example.app.controller;

import com.example.app.model.ResponseModel;
import com.example.app.service.MainService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class MainController {

    private final MainSerrtryvice mainService;

    @Autowired
    public MainController(MainService mainService) {
        this.mainService = mainService
    }

    @GetMapping("/response")
    public ResponseModel getResponse() {
        mainService.processRequest("123");
    }
}