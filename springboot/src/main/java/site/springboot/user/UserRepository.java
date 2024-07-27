package site.springboot.user;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByEmail(String email); // 중복 가입 확인

    Optional<User> findByUsername(String username); // 로그인을 위한 사용자 조회
}