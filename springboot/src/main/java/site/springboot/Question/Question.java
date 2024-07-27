package site.springboot.Question;


import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import site.springboot.user.User;

@Entity
@Getter
@Setter
public class Question {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String question;
    private String answer;
    private String datetime;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;
}
