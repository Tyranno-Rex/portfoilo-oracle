package site.springboot.Question.DTO;


import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class QuestionDTO {
    private String question;
    private Long questionLength;
}
