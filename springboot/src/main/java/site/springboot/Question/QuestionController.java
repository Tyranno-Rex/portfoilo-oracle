package site.springboot.Question;


import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import site.springboot.Question.DTO.QuestionDTO;

import java.security.Principal;

@RestController
@RequiredArgsConstructor
@RequestMapping("/question")
public class QuestionController {

    private final QuestionService questionService;

    @PostMapping("/send")
    public String receviedQuestion(@RequestBody QuestionDTO questionDTO, Principal principal) {

        Question question = new Question();
        boolean Flag_saveReceivedQuestion = questionService.saveReceviedQuestion(questionDTO, principal);

        if (Flag_saveReceivedQuestion) {
            return "success";
        } else {
            return "fail";
        }
    }
}
