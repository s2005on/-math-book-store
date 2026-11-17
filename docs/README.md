# Bộ tài liệu đồ án LTD's Book Store

Tài liệu kỹ thuật, quản lý dự án, kiểm thử và bàn giao của **LTD's Book Store**. [Quay về README chính](../README.md).

> **Phân biệt phiên bản:** nguồn `main` hiện là **v0.5.1**; ZIP **v1.2.1 Auth Update** được kiểm tra riêng trên máy và **chưa đồng bộ toàn bộ code/ảnh lên GitHub**. Xem [đối chiếu](REPO-SYNC-STATUS.md). Mọi bằng chứng cần gắn với đúng commit.

## 1. Bắt đầu và tổng quan

| Nội dung | Liên kết |
|---|---|
| Giới thiệu, cấu trúc thư mục, sơ đồ hệ thống | [README dự án](../README.md) |
| Cài và khởi động trên Windows | [START-HERE.md](../START-HERE.md) |
| Kiến trúc API/SQLite | [03 — System Design](03-system-design.md) |
| Trạng thái ZIP và mã trên GitHub | [REPO-SYNC-STATUS.md](REPO-SYNC-STATUS.md) |
| Tiếp nhận phiên bản v1.2.1 | [RELEASE-INTAKE-v1.2.1.md](RELEASE-INTAKE-v1.2.1.md) |

## 2. Phân tích yêu cầu và thiết kế

| Hồ sơ | Nội dung |
|---|---|
| [01 — Project Charter](01-project-charter.md) | Mục tiêu, phạm vi, tiêu chí nghiệm thu |
| [02 — Requirements](02-requirements.md) | Yêu cầu chức năng và User Stories |
| [03 — System Design](03-system-design.md) | Kiến trúc, API, bảng dữ liệu |
| [04 — WBS](04-wbs.md) | Phân rã công việc |
| [05 — Schedule](05-schedule.md) | Mốc tiến độ |
| [08 — MVP Demo](08-mvp-demo.md) | Kịch bản trình diễn giai đoạn đầu |

## 3. Quản lý đồ án và làm việc nhóm

| Hồ sơ | Nội dung |
|---|---|
| [06 — Scrum / Team](06-scrum-team.md) | Vai trò, nguyên tắc làm việc |
| [07 — Sprint 0 Backlog](07-sprint-0-backlog.md) | Backlog giai đoạn khởi động |
| [Sprint Tracker](SPRINT-TRACKER.md) | Mục tiêu Sprint, Issue/PR, công việc còn lại |
| [Team](TEAM.md) · [Stakeholders](STAKEHOLDERS.md) | Trách nhiệm, bên liên quan |
| [Risks](RISKS.md) · [Quality](QUALITY.md) | Rủi ro, tiêu chí chất lượng |
| [Configuration](CONFIG.md) | Quản lý cấu hình và dữ liệu |

## 4. Git, kiểm thử và phát hành

| Tài liệu | Nội dung |
|---|---|
| [Workflow](WORKFLOW.md) | Issue → branch → PR → CI → merge → release |
| [Git conventions](GIT.md) · [PR review](PR-REVIEW.md) | Quy tắc nhánh/commit, review |
| [Test Plan](TEST-PLAN.md) | Test cases, kiểm tra responsive, phân quyền |
| [Academic Traceability](ACADEMIC-TRACEABILITY.md) | User Story ↔ bằng chứng ↔ chức năng |
| [Evidence folder](evidence/README.md) | Nơi lưu ảnh/log kiểm thử thật |
| [Version Intake](VERSION-INTAKE.md) | Quy trình nhận ZIP mới |
| [Versioning](VERSIONING.md) · [Release Checklist](RELEASE-CHECKLIST.md) | SemVer, điều kiện tạo tag |
| [Changelog](../CHANGELOG.md) · [GitHub Actions](https://github.com/s2005on/LTDs-Book-Store/actions) | Lịch sử và kết quả CI |

## 5. Báo cáo học phần và bàn giao

| Hồ sơ | Nội dung |
|---|---|
| [B2 Report](B2-REPORT.md) | Môi trường, kỹ thuật và minh chứng |
| [Midterm](MIDTERM.md) | Khung báo cáo giữa kỳ |
| [Sprint 0 Report](SPRINT0-REPORT.md) | Dấu mốc lịch sử ban đầu |
| [Final Report](FINAL-REPORT.md) | Kết quả, thiết kế, hạn chế |
| [Final Handover](FINAL-HANDOVER.md) | Kiểm tra trước bàn giao |
| [Verification](../VERIFICATION.md) | Kết quả xác minh và giới hạn |
| [Release notes v0.2.0](RELEASE-v0.2.0.md) | Hồ sơ mốc cũ, không đại diện cho bản mới |

## 6. Hướng dẫn lưu minh chứng phục vụ giảng viên

Mỗi lần phát triển/kiểm thử một bản:

1. Ghi **tên ZIP, VERSION, commit SHA, ngày, hệ điều hành**.
2. Kèm Issue/PR liên quan, ảnh giao diện desktop/mobile và kết quả Python/JavaScript.
3. Chỉ đánh dấu **Đạt** khi tự chạy kiểm thử hoặc có CI của **đúng commit**.
4. Che thông tin cá nhân, không đưa `.env`, SQLite thật hay token lên GitHub.
5. Bản ZIP mới được nhập vào nhánh riêng, kiểm tra CI, merge rồi mới tạo GitHub Release.

**VPS đang tạm hoãn.** Thư mục `deploy/` chỉ phục vụ tài liệu kỹ thuật trong giai đoạn đồ án.
