package site.springboot.Question;


import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import site.springboot.Question.DTO.QuestionDTO;
import site.springboot.user.User;
import site.springboot.user.UserRepository;

import java.security.Principal;
import java.time.LocalDateTime;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class QuestionService {

    private final QuestionRepository questionRepository;
    private final UserRepository userRepository;
    public Boolean saveReceviedQuestion(QuestionDTO questionDTO, Principal principal) {
        Question question = new Question();
        question.setQuestion(questionDTO.getQuestion());
        question.setDatetime(LocalDateTime.now().toString());

        try {
            Optional<User> user = userRepository.findByName(principal.getName());
            question.setUser(user.get());
            questionRepository.save(question);
            return true;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }
}
